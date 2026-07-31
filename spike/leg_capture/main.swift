// P0 live-leg capture tool.
//
//   leg-capture online <outdir> [seconds]
//     Records the Lark ("Wireless" input device) to me.wav and system audio
//     (ScreenCaptureKit) to them.wav, simultaneously. Leg 1.
//   leg-capture single <device-substring> <outdir> [seconds]
//     Records one input device to mix.wav. Leg 2 (Lark) / leg 3 (built-in mic).
//
// Prints a level line every 5 s (the "audio is flowing" sanity indicator).
// Stops after [seconds] or on Ctrl-C; both paths finalize the wav headers.
// Runbooks: docs/leg-1-online.md, docs/leg-2-inperson.md

import Foundation
import AVFoundation
import CoreAudio
import ScreenCaptureKit

setvbuf(stdout, nil, _IONBF, 0)

func fail(_ msg: String) -> Never { print("CAPTURE FAILED: \(msg)"); exit(1) }

// ---- arguments ------------------------------------------------------------
let argv = CommandLine.arguments
var mode = "", needle = "Wireless", outDirPath = "", maxSeconds = 3 * 3600
if argv.count >= 3, argv[1] == "online" {
    mode = "online"; outDirPath = argv[2]
    if argv.count >= 4 { maxSeconds = Int(argv[3]) ?? maxSeconds }
} else if argv.count >= 4, argv[1] == "single" {
    mode = "single"; needle = argv[2]; outDirPath = argv[3]
    if argv.count >= 5 { maxSeconds = Int(argv[4]) ?? maxSeconds }
} else {
    print("usage: leg-capture online <outdir> [seconds]")
    print("       leg-capture single <device-substring> <outdir> [seconds]")
    exit(1)
}
let outDir = URL(fileURLWithPath: outDirPath)
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)

// ---- shared plumbing ------------------------------------------------------
final class Meter {
    private let lock = NSLock()
    private var sumSq: Float = 0
    private var frames = 0
    func add(_ pcm: AVAudioPCMBuffer) {
        guard let data = pcm.floatChannelData else { return }
        let n = Int(pcm.frameLength), ch = Int(pcm.format.channelCount)
        var s: Float = 0
        for c in 0..<ch { for i in 0..<n { let v = data[c][i]; s += v * v } }
        lock.lock(); sumSq += s / Float(ch); frames += n; lock.unlock()
    }
    func drainDb() -> Float {
        lock.lock(); defer { lock.unlock() }
        let db: Float = frames > 0
            ? 20 * log10(max((sumSq / Float(frames)).squareRoot(), 1e-9)) : -180
        sumSq = 0; frames = 0
        return db
    }
}

final class Writer {
    private let lock = NSLock()
    private var file: AVAudioFile?
    private var frames = 0
    private var rate: Double = 48000
    let url: URL
    init(_ url: URL) { self.url = url }
    func write(_ pcm: AVAudioPCMBuffer) {
        lock.lock(); defer { lock.unlock() }
        if file == nil {
            file = try? AVAudioFile(forWriting: url, settings: pcm.format.settings)
            rate = pcm.format.sampleRate
        }
        try? file?.write(from: pcm)
        frames += Int(pcm.frameLength)
    }
    func finalize() -> Double {  // returns seconds written; nils file -> header valid
        lock.lock(); defer { lock.unlock() }
        file = nil
        return Double(frames) / rate
    }
}

func pcmBuffer(from sampleBuffer: CMSampleBuffer) -> AVAudioPCMBuffer? {
    guard let desc = CMSampleBufferGetFormatDescription(sampleBuffer),
          let asbd = CMAudioFormatDescriptionGetStreamBasicDescription(desc),
          let format = AVAudioFormat(streamDescription: asbd) else { return nil }
    let frames = CMSampleBufferGetNumSamples(sampleBuffer)
    guard frames > 0,
          let pcm = AVAudioPCMBuffer(pcmFormat: format,
                                     frameCapacity: AVAudioFrameCount(frames)) else { return nil }
    pcm.frameLength = AVAudioFrameCount(frames)
    guard CMSampleBufferCopyPCMDataIntoAudioBufferList(
        sampleBuffer, at: 0, frameCount: Int32(frames),
        into: pcm.mutableAudioBufferList) == noErr else { return nil }
    return pcm
}

func inputDeviceID(matching needle: String) -> (AudioDeviceID, String)? {
    var addr = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyDevices,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain)
    var size: UInt32 = 0
    guard AudioObjectGetPropertyDataSize(
        AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil, &size) == noErr else { return nil }
    var ids = [AudioDeviceID](repeating: 0, count: Int(size) / MemoryLayout<AudioDeviceID>.size)
    guard AudioObjectGetPropertyData(
        AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil, &size, &ids) == noErr else { return nil }
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
        if status == noErr, let n = name as String?,
           n.localizedCaseInsensitiveContains(needle) { return (id, n) }
    }
    return nil
}

// ---- capture pieces -------------------------------------------------------
let done = DispatchSemaphore(value: 0)

final class SystemAudioTap: NSObject, SCStreamOutput, SCStreamDelegate {
    let writer: Writer
    let meter: Meter
    init(writer: Writer, meter: Meter) { self.writer = writer; self.meter = meter }
    func stream(_ stream: SCStream, didOutputSampleBuffer sb: CMSampleBuffer,
                of type: SCStreamOutputType) {
        guard type == .audio, let pcm = pcmBuffer(from: sb) else { return }
        writer.write(pcm)
        meter.add(pcm)
    }
    func stream(_ stream: SCStream, didStopWithError error: Error) {
        print("CAPTURE FAILED: system-audio stream stopped: \(error.localizedDescription)")
        done.signal()
    }
}

var writers: [(String, Writer)] = []
var meters: [(String, Meter)] = []
var engine: AVAudioEngine?
var sckStream: SCStream?
var sckTap: SystemAudioTap?

func startEngineCapture(label: String, fileName: String) {
    guard let (devID, devName) = inputDeviceID(matching: needle) else {
        fail("no input device name contains \"\(needle)\" — is it plugged in?")
    }
    let eng = AVAudioEngine()
    let input = eng.inputNode
    guard let unit = input.audioUnit else { fail("no input audio unit") }
    var dev = devID
    guard AudioUnitSetProperty(unit, kAudioOutputUnitProperty_CurrentDevice,
                               kAudioUnitScope_Global, 0, &dev,
                               UInt32(MemoryLayout<AudioDeviceID>.size)) == noErr else {
        fail("could not select device \"\(devName)\"")
    }
    let format = input.inputFormat(forBus: 0)
    let writer = Writer(outDir.appendingPathComponent(fileName))
    let meter = Meter()
    writers.append((label, writer)); meters.append((label, meter))
    input.installTap(onBus: 0, bufferSize: 4096, format: format) { pcm, _ in
        writer.write(pcm)
        meter.add(pcm)
    }
    do { try eng.start() } catch { fail("engine start: \(error.localizedDescription)") }
    engine = eng
    print("\(label): \(devName) — \(format.channelCount) ch @ \(Int(format.sampleRate)) Hz → \(fileName)")
}

func startSystemCapture() {
    let writer = Writer(outDir.appendingPathComponent("them.wav"))
    let meter = Meter()
    writers.append(("THEM", writer)); meters.append(("THEM", meter))
    let tap = SystemAudioTap(writer: writer, meter: meter)
    sckTap = tap
    let ready = DispatchSemaphore(value: 0)
    var startError: String?
    Task {
        do {
            let content = try await SCShareableContent.excludingDesktopWindows(
                false, onScreenWindowsOnly: true)
            guard let display = content.displays.first else {
                startError = "no display found"; ready.signal(); return
            }
            let cfg = SCStreamConfiguration()
            cfg.capturesAudio = true
            cfg.excludesCurrentProcessAudio = true
            cfg.sampleRate = 48000
            cfg.channelCount = 2
            cfg.width = 64; cfg.height = 64
            cfg.minimumFrameInterval = CMTime(value: 1, timescale: 1)
            let stream = SCStream(filter: SCContentFilter(display: display, excludingWindows: []),
                                  configuration: cfg, delegate: tap)
            try stream.addStreamOutput(tap, type: .audio,
                                       sampleHandlerQueue: DispatchQueue(label: "sck-audio"))
            try await stream.startCapture()
            sckStream = stream
        } catch {
            startError = error.localizedDescription
        }
        ready.signal()
    }
    ready.wait()
    if let e = startError { fail("system-audio capture: \(e)") }
    print("THEM: system audio (ScreenCaptureKit) — 2 ch @ 48000 Hz → them.wav")
}

// ---- start ----------------------------------------------------------------
switch mode {
case "online":
    startSystemCapture()
    startEngineCapture(label: "ME", fileName: "me.wav")
default:
    startEngineCapture(label: "MIX", fileName: "mix.wav")
}
print("capturing → \(outDir.path)  (Ctrl-C to stop\(maxSeconds < 3 * 3600 ? ", auto-stop \(maxSeconds)s" : ""))")

// level line every 5 s, auto-stop check every 1 s
var elapsed = 0
let timerQueue = DispatchQueue(label: "meter-timer")
let timer = DispatchSource.makeTimerSource(queue: timerQueue)
timer.schedule(deadline: .now() + 1, repeating: 1)
timer.setEventHandler {
    elapsed += 1
    if elapsed % 5 == 0 {
        let parts = meters.map { (label, m) in
            String(format: "%@ %6.1f dBFS", label, m.drainDb())
        }
        print(String(format: "t+%02d:%02d  ", elapsed / 60, elapsed % 60)
              + parts.joined(separator: " | "))
    }
    if elapsed >= maxSeconds { done.signal() }
}
timer.resume()

// Ctrl-C -> clean stop
signal(SIGINT, SIG_IGN)
let sigSrc = DispatchSource.makeSignalSource(signal: SIGINT, queue: DispatchQueue(label: "sig"))
sigSrc.setEventHandler { print("\nCtrl-C — stopping…"); done.signal() }
sigSrc.resume()

done.wait()
timer.cancel()
engine?.stop()
engine?.inputNode.removeTap(onBus: 0)
if let s = sckStream {
    let stopped = DispatchSemaphore(value: 0)
    Task { try? await s.stopCapture(); stopped.signal() }
    stopped.wait()
}
var summary: [String] = []
for (label, w) in writers {
    let secs = w.finalize()
    summary.append(String(format: "%@ %.1fs → %@", label, secs, w.url.lastPathComponent))
}
print("stopped cleanly — files finalized: " + summary.joined(separator: ", "))
