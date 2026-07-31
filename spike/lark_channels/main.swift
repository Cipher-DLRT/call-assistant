// P0 check (b): what does the Lark M2 USB-C receiver present, and do TX1/TX2
// arrive as separate left/right channels?
//
// Records N seconds (default 20, first arg) from the input device whose name
// contains "Wireless" (or second arg as name substring), prints a per-second
// L/R level meter, writes lark.wav to the current directory.
// Runbook: docs/runbook-p0b-lark-channels.md

import Foundation
import AVFoundation
import CoreAudio

setvbuf(stdout, nil, _IONBF, 0)

let seconds = CommandLine.arguments.count > 1 ? (Int(CommandLine.arguments[1]) ?? 20) : 20
let nameNeedle = CommandLine.arguments.count > 2 ? CommandLine.arguments[2] : "Wireless"
let outURL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
    .appendingPathComponent("lark.wav")

func inputDevices() -> [(AudioDeviceID, String)] {
    var addr = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDevices,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain)
    var size: UInt32 = 0
    guard AudioObjectGetPropertyDataSize(
        AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil, &size) == noErr else { return [] }
    var ids = [AudioDeviceID](repeating: 0, count: Int(size) / MemoryLayout<AudioDeviceID>.size)
    guard AudioObjectGetPropertyData(
        AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil, &size, &ids) == noErr else { return [] }
    var out: [(AudioDeviceID, String)] = []
    for id in ids {
        var nameAddr = AudioObjectPropertyAddress(
            mSelector: kAudioObjectPropertyName,
            mScope: kAudioObjectPropertyScopeGlobal,
            mElement: kAudioObjectPropertyElementMain)
        var name: CFString? = nil
        var nameSize = UInt32(MemoryLayout<CFString?>.size)
        let status = withUnsafeMutablePointer(to: &name) {
            AudioObjectGetPropertyData(id, &nameAddr, 0, nil, &nameSize, $0)
        }
        if status == noErr, let n = name as String? { out.append((id, n)) }
    }
    return out
}

let devices = inputDevices()
guard var deviceID = devices.first(where: { $0.1.localizedCaseInsensitiveContains(nameNeedle) })?.0
else {
    print("DEVICE NOT FOUND: no audio device name contains \"\(nameNeedle)\". Devices seen:")
    for (_, n) in devices { print("  - \(n)") }
    exit(1)
}
let deviceName = devices.first(where: { $0.0 == deviceID })!.1

// Microphone permission (prompts on first run, naming the terminal app).
let permSem = DispatchSemaphore(value: 0)
var granted = false
AVCaptureDevice.requestAccess(for: .audio) { g in granted = g; permSem.signal() }
permSem.wait()
guard granted else {
    print("CAPTURE FAILED: microphone permission denied. System Settings → " +
          "Privacy & Security → Microphone → enable your terminal app, then re-run.")
    exit(1)
}

let engine = AVAudioEngine()
let input = engine.inputNode
guard let unit = input.audioUnit else { print("CAPTURE FAILED: no input audio unit"); exit(1) }
guard AudioUnitSetProperty(unit, kAudioOutputUnitProperty_CurrentDevice,
                           kAudioUnitScope_Global, 0, &deviceID,
                           UInt32(MemoryLayout<AudioDeviceID>.size)) == noErr else {
    print("CAPTURE FAILED: could not select device \"\(deviceName)\"")
    exit(1)
}

let format = input.inputFormat(forBus: 0)
let channels = Int(format.channelCount)
let rate = format.sampleRate
print("recording from: \(deviceName) — \(channels) ch @ \(Int(rate)) Hz, \(seconds) s")
if channels < 2 {
    print("NOTE: device presents only \(channels) channel(s) — no L/R split possible in this mode.")
}

var file: AVAudioFile?
do { file = try AVAudioFile(forWriting: outURL, settings: format.settings) }
catch {
    print("CAPTURE FAILED: cannot write \(outURL.path): \(error.localizedDescription)")
    exit(1)
}

final class Meter {
    var sumSq: [Float]
    var frames = 0
    var second = 0
    let done = DispatchSemaphore(value: 0)
    init(channels: Int) { sumSq = [Float](repeating: 0, count: channels) }
}
let meter = Meter(channels: channels)

input.installTap(onBus: 0, bufferSize: 4096, format: format) { buffer, _ in
    try? file?.write(from: buffer)
    guard let data = buffer.floatChannelData else { return }
    let n = Int(buffer.frameLength)
    for ch in 0..<channels {
        var s: Float = 0
        for i in 0..<n { let v = data[ch][i]; s += v * v }
        meter.sumSq[ch] += s
    }
    meter.frames += n
    if meter.frames >= Int(rate) {
        meter.second += 1
        let dbs = meter.sumSq.map { s -> Float in
            20 * log10(max((s / Float(meter.frames)).squareRoot(), 1e-9))
        }
        let parts = dbs.enumerated().map { (i, db) in
            String(format: "%@ %6.1f dBFS", i == 0 ? "L" : (i == 1 ? "R" : "ch\(i)"), db)
        }
        print(String(format: "t+%02ds  ", meter.second) + parts.joined(separator: " | "))
        meter.sumSq = [Float](repeating: 0, count: channels)
        meter.frames = 0
        if meter.second >= seconds { meter.done.signal() }
    }
}

do { try engine.start() } catch {
    print("CAPTURE FAILED: engine start: \(error.localizedDescription)")
    exit(1)
}

meter.done.wait()
engine.stop()
input.removeTap(onBus: 0)
file = nil  // finalize the wav header before exiting
print("done — wav written to \(outURL.path)")
