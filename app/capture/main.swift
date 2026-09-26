// P1 capture — extended from spike/leg_capture/main.swift (P0 evidence code).
//
// File modes (unchanged from leg-capture):
//   capture online <outdir> [seconds]            me.wav (mic) + them.wav (SCK)
//   capture single <device-substring> <outdir> [seconds]   mix.wav
//
// Stream modes (P1 loop): resample each stream to 16 kHz mono s16 and write
// framed binary to STDOUT: [u8 stream_id][u32 LE n_samples][s16le payload].
// Stream 0 = mic (ME online / the room in-person), stream 1 = system audio.
// Status + level lines go to STDERR. Ctrl-C -> clean stop.
//   capture stream-online              mic + system audio (law 8 channel split;
//                                      Lark auto-preferred when present, else built-in)
//   capture stream-online --exclude-pid <pid>[,<pid>…]
//                                      stream 1 from a Core Audio process tap of all
//                                      system audio except the listed processes (e.g.
//                                      the caller's own mixer); PIDs that open audio
//                                      later are excluded within 2 s (macOS 14.2+)
//   capture stream-inperson            built-in mic only (primary rig, law 8)

import Foundation
import AVFoundation
import CoreAudio
import ScreenCaptureKit

setvbuf(stdout, nil, _IONBF, 0)

let argv = CommandLine.arguments
var mode = "", needle = "Wireless", outDirPath = "", maxSeconds = 3 * 3600
var excludePIDs: [pid_t] = []   // stream-online --exclude-pid: empty = today's SCK path
switch argv.count >= 2 ? argv[1] : "" {
case "online" where argv.count >= 3:
    mode = "online"; outDirPath = argv[2]
    if argv.count >= 4 { maxSeconds = Int(argv[3]) ?? maxSeconds }
case "single" where argv.count >= 4:
    mode = "single"; needle = argv[2]; outDirPath = argv[3]
    if argv.count >= 5 { maxSeconds = Int(argv[4]) ?? maxSeconds }
case "stream-online" where argv.count == 2:
    mode = "stream-online"
case "stream-online" where argv.count == 4 && argv[2] == "--exclude-pid":
    let pids = argv[3].split(separator: ",").map { pid_t($0.trimmingCharacters(in: .whitespaces)) }
    if !pids.isEmpty && !pids.contains(nil) { mode = "stream-online"; excludePIDs = pids.map { $0! } }
case "stream-inperson":
    mode = "stream-inperson"; needle = "MacBook"
default: break
}
if mode.isEmpty {
    FileHandle.standardError.write("""
    usage: capture online <outdir> [seconds]
           capture single <device-substring> <outdir> [seconds]
           capture stream-online [--exclude-pid <pid>[,<pid>…]]
           capture stream-inperson

    """.data(using: .utf8)!)
    exit(1)
}
let isStream = mode.hasPrefix("stream-")

func note(_ msg: String) {
    if isStream { FileHandle.standardError.write((msg + "\n").data(using: .utf8)!) }
    else { print(msg) }
}
func fail(_ msg: String) -> Never { note("CAPTURE FAILED: \(msg)"); exit(1) }

let outDir = URL(fileURLWithPath: outDirPath.isEmpty ? "." : outDirPath)
if !isStream {
    try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
}

// ---- shared plumbing (unchanged from leg-capture) -------------------------
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
    func finalize() -> Double {  // nils file -> header valid (P0 fix)
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

// ---- stream plumbing (P1) -------------------------------------------------
final class FrameWriter {
    private let lock = NSLock()
    private let out = FileHandle.standardOutput
    func write(streamId: UInt8, samples: [Int16]) {
        guard !samples.isEmpty else { return }
        var data = Data()
        data.append(streamId)
        var n = UInt32(samples.count).littleEndian
        withUnsafeBytes(of: &n) { data.append(contentsOf: $0) }
        samples.withUnsafeBytes { data.append(contentsOf: $0) }
        lock.lock(); out.write(data); lock.unlock()
    }
}
let frameWriter = FrameWriter()

// Stateful per-stream resampler: any input format -> 16 kHz mono s16.
final class Resampler {
    private var converter: AVAudioConverter?
    private let target = AVAudioFormat(commonFormat: .pcmFormatInt16, sampleRate: 16000,
                                       channels: 1, interleaved: true)!
    func convert(_ pcm: AVAudioPCMBuffer) -> [Int16] {
        if converter == nil { converter = AVAudioConverter(from: pcm.format, to: target) }
        guard let conv = converter else { return [] }
        let capacity = AVAudioFrameCount(Double(pcm.frameLength)
                                         * 16000.0 / pcm.format.sampleRate) + 64
        guard let outBuf = AVAudioPCMBuffer(pcmFormat: target, frameCapacity: capacity)
        else { return [] }
        var consumed = false
        var err: NSError?
        let status = conv.convert(to: outBuf, error: &err) { _, outStatus in
            if consumed { outStatus.pointee = .noDataNow; return nil }
            consumed = true; outStatus.pointee = .haveData; return pcm
        }
        guard status != .error, let ch = outBuf.int16ChannelData else { return [] }
        return Array(UnsafeBufferPointer(start: ch[0], count: Int(outBuf.frameLength)))
    }
}

// ---- capture pieces -------------------------------------------------------
let done = DispatchSemaphore(value: 0)

final class SystemAudioTap: NSObject, SCStreamOutput, SCStreamDelegate {
    let meter: Meter
    let writer: Writer?          // file mode
    let streamId: UInt8?         // stream mode
    private let resampler = Resampler()
    init(writer: Writer?, meter: Meter, streamId: UInt8?) {
        self.writer = writer; self.meter = meter; self.streamId = streamId
    }
    func stream(_ stream: SCStream, didOutputSampleBuffer sb: CMSampleBuffer,
                of type: SCStreamOutputType) {
        guard type == .audio, let pcm = pcmBuffer(from: sb) else { return }
        writer?.write(pcm)
        meter.add(pcm)
        if let id = streamId { frameWriter.write(streamId: id, samples: resampler.convert(pcm)) }
    }
    func stream(_ stream: SCStream, didStopWithError error: Error) {
        note("CAPTURE FAILED: system-audio stream stopped: \(error.localizedDescription)")
        done.signal()
    }
}

var writers: [(String, Writer)] = []
var meters: [(String, Meter)] = []
var engine: AVAudioEngine?
var sckStream: SCStream?
var sckTap: SystemAudioTap?

func startEngineCapture(label: String, fileName: String?, streamId: UInt8?) {
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
    let writer = fileName.map { Writer(outDir.appendingPathComponent($0)) }
    let meter = Meter()
    if let w = writer { writers.append((label, w)) }
    meters.append((label, meter))
    let resampler = Resampler()
    input.installTap(onBus: 0, bufferSize: 4096, format: format) { pcm, _ in
        writer?.write(pcm)
        meter.add(pcm)
        if let id = streamId { frameWriter.write(streamId: id, samples: resampler.convert(pcm)) }
    }
    do { try eng.start() } catch { fail("engine start: \(error.localizedDescription)") }
    engine = eng
    let sink = fileName ?? "stream \(streamId ?? 0)"
    note("\(label): \(devName) — \(format.channelCount) ch @ \(Int(format.sampleRate)) Hz → \(sink)")
}

func startSystemCapture(streamId: UInt8?) {
    let writer = streamId == nil ? Writer(outDir.appendingPathComponent("them.wav")) : nil
    let meter = Meter()
    if let w = writer { writers.append(("THEM", w)) }
    meters.append(("THEM", meter))
    let tap = SystemAudioTap(writer: writer, meter: meter, streamId: streamId)
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
    note("THEM: system audio (ScreenCaptureKit) — 2 ch @ 48000 Hz → \(streamId == nil ? "them.wav" : "stream 1")")
}

// --exclude-pid: a global stereo Core Audio process tap minus the listed processes,
// read through a private aggregate device. A PID has an audio process object only once
// it has opened audio, so the list is re-resolved on the meter timer and the tap's
// description updated in place (no restart; stream 1 continues).
var tapID = AudioObjectID(kAudioObjectUnknown)
var tapDesc: CATapDescription?
var tapDevice = AudioObjectID(kAudioObjectUnknown)
var tapProc: AudioDeviceIOProcID?
var tapExcluded: [AudioObjectID] = []

func processObject(pid: pid_t) -> AudioObjectID? {
    var addr = AudioObjectPropertyAddress(
        mSelector: kAudioHardwarePropertyTranslatePIDToProcessObject,
        mScope: kAudioObjectPropertyScopeGlobal,
        mElement: kAudioObjectPropertyElementMain)
    var p = pid, obj = AudioObjectID(kAudioObjectUnknown)
    var size = UInt32(MemoryLayout<AudioObjectID>.size)
    let status = AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &addr,
                                            UInt32(MemoryLayout<pid_t>.size), &p, &size, &obj)
    return status == noErr && obj != kAudioObjectUnknown ? obj : nil
}

// Resolves the PIDs; returns the process objects and one stderr line when the set changed.
func resolveExcluded() -> ([AudioObjectID], String?) {
    let found = excludePIDs.map { ($0, processObject(pid: $0)) }
    let objs = found.compactMap { $0.1 }
    guard objs != tapExcluded || tapDesc == nil else { return (objs, nil) }
    let on = found.filter { $0.1 != nil }.map { String($0.0) }
    let off = found.filter { $0.1 == nil }.map { String($0.0) }
    return (objs, "THEM exclude: excluding pid [\(on.joined(separator: ","))]"
                + " no audio yet [\(off.joined(separator: ","))]")
}

func refreshExcluded() {
    guard let desc = tapDesc else { return }
    let (objs, line) = resolveExcluded()
    guard let line = line else { return }
    desc.processes = objs
    var addr = AudioObjectPropertyAddress(mSelector: kAudioTapPropertyDescription,
                                          mScope: kAudioObjectPropertyScopeGlobal,
                                          mElement: kAudioObjectPropertyElementMain)
    var ref = Unmanaged.passUnretained(desc).toOpaque()   // the property holds an object reference
    let status = AudioObjectSetPropertyData(tapID, &addr, 0, nil,
                                            UInt32(MemoryLayout<UnsafeMutableRawPointer>.size), &ref)
    if status == noErr { tapExcluded = objs; note(line) }
    else { note("THEM exclude: tap update failed (OSStatus \(status))") }
}

func defaultOutputUID() -> String? {
    var addr = AudioObjectPropertyAddress(mSelector: kAudioHardwarePropertyDefaultSystemOutputDevice,
                                          mScope: kAudioObjectPropertyScopeGlobal,
                                          mElement: kAudioObjectPropertyElementMain)
    var dev = AudioObjectID(kAudioObjectUnknown)
    var size = UInt32(MemoryLayout<AudioObjectID>.size)
    guard AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil,
                                     &size, &dev) == noErr else { return nil }
    addr.mSelector = kAudioDevicePropertyDeviceUID
    var uid: CFString? = nil
    size = UInt32(MemoryLayout<CFString?>.size)
    let status = withUnsafeMutablePointer(to: &uid) {
        AudioObjectGetPropertyData(dev, &addr, 0, nil, &size, $0)
    }
    return status == noErr ? uid as String? : nil
}

func startProcessTapCapture(streamId: UInt8) {
    let meter = Meter()
    meters.append(("THEM", meter))
    let (objs, line) = resolveExcluded()
    let desc = CATapDescription(stereoGlobalTapButExcludeProcesses: objs)
    desc.uuid = UUID(); desc.isPrivate = true; desc.muteBehavior = .unmuted
    guard AudioHardwareCreateProcessTap(desc, &tapID) == noErr else { fail("process tap: create") }
    tapDesc = desc; tapExcluded = objs
    if let l = line { note(l) }
    var addr = AudioObjectPropertyAddress(mSelector: kAudioTapPropertyFormat,
                                          mScope: kAudioObjectPropertyScopeGlobal,
                                          mElement: kAudioObjectPropertyElementMain)
    var asbd = AudioStreamBasicDescription()
    var size = UInt32(MemoryLayout<AudioStreamBasicDescription>.size)
    guard AudioObjectGetPropertyData(tapID, &addr, 0, nil, &size, &asbd) == noErr,
          let format = AVAudioFormat(streamDescription: &asbd) else { fail("process tap: format") }
    // Stream 1 must keep flowing in silence, like SCK's. Measured: with tap auto-start the
    // IOProc is never called while no non-excluded process does audio I/O. Auto-start off
    // plus the default output device as the clock gives continuous frames.
    guard let outUID = defaultOutputUID() else { fail("process tap: no default output device") }
    let agg: [String: Any] = [
        kAudioAggregateDeviceNameKey: "capture-tap",
        kAudioAggregateDeviceUIDKey: UUID().uuidString,
        kAudioAggregateDeviceMainSubDeviceKey: outUID,
        kAudioAggregateDeviceSubDeviceListKey: [[kAudioSubDeviceUIDKey: outUID]],
        kAudioAggregateDeviceIsPrivateKey: true,
        kAudioAggregateDeviceIsStackedKey: false,
        kAudioAggregateDeviceTapAutoStartKey: false,
        kAudioAggregateDeviceTapListKey: [[kAudioSubTapDriftCompensationKey: true,
                                           kAudioSubTapUIDKey: desc.uuid.uuidString]]]
    guard AudioHardwareCreateAggregateDevice(agg as CFDictionary, &tapDevice) == noErr else {
        fail("process tap: aggregate device")
    }
    let resampler = Resampler()
    let ioBlock: AudioDeviceIOBlock = { _, inData, _, _, _ in
        guard let pcm = AVAudioPCMBuffer(pcmFormat: format, bufferListNoCopy: inData) else { return }
        meter.add(pcm)
        frameWriter.write(streamId: streamId, samples: resampler.convert(pcm))
    }
    guard AudioDeviceCreateIOProcIDWithBlock(&tapProc, tapDevice, DispatchQueue(label: "tap-audio"),
                                             ioBlock) == noErr,
          AudioDeviceStart(tapDevice, tapProc) == noErr else { fail("process tap: start") }
    note("THEM: system audio (Core Audio process tap) — \(format.channelCount) ch @ "
         + "\(Int(format.sampleRate)) Hz → stream \(streamId)")
}

func stopProcessTapCapture() {
    guard tapDesc != nil else { return }
    AudioDeviceStop(tapDevice, tapProc)
    if let p = tapProc { AudioDeviceDestroyIOProcID(tapDevice, p) }
    AudioHardwareDestroyAggregateDevice(tapDevice)
    AudioHardwareDestroyProcessTap(tapID)
}

// ---- start ----------------------------------------------------------------
switch mode {
case "online":
    startSystemCapture(streamId: nil)
    startEngineCapture(label: "ME", fileName: "me.wav", streamId: nil)
case "single":
    startEngineCapture(label: "MIX", fileName: "mix.wav", streamId: nil)
case "stream-online":
    // law 8: Lark auto-preferred when worn, built-in is the standing rig
    if inputDeviceID(matching: "Wireless") == nil { needle = "MacBook" }
    if excludePIDs.isEmpty {
        startSystemCapture(streamId: 1)
        startEngineCapture(label: "ME", fileName: nil, streamId: 0)
    } else {  // mic first: starting the mic engine after the tap device deadlocks in the HAL
        startEngineCapture(label: "ME", fileName: nil, streamId: 0)
        startProcessTapCapture(streamId: 1)
    }
default:  // stream-inperson
    startEngineCapture(label: "MIX", fileName: nil, streamId: 0)
}
note(isStream ? "streaming (Ctrl-C to stop)"
     : "capturing → \(outDir.path)  (Ctrl-C to stop\(maxSeconds < 3 * 3600 ? ", auto-stop \(maxSeconds)s" : ""))")

var elapsed = 0
let timerQueue = DispatchQueue(label: "meter-timer")
let timer = DispatchSource.makeTimerSource(queue: timerQueue)
timer.schedule(deadline: .now() + 1, repeating: 1)
timer.setEventHandler {
    elapsed += 1
    if !excludePIDs.isEmpty && elapsed % 2 == 0 { refreshExcluded() }
    if elapsed % 5 == 0 {
        let parts = meters.map { (label, m) in
            String(format: "%@ %6.1f dBFS", label, m.drainDb())
        }
        note(String(format: "t+%02d:%02d  ", elapsed / 60, elapsed % 60)
             + parts.joined(separator: " | "))
    }
    if !isStream && elapsed >= maxSeconds { done.signal() }
}
timer.resume()

signal(SIGINT, SIG_IGN)
let sigSrc = DispatchSource.makeSignalSource(signal: SIGINT, queue: DispatchQueue(label: "sig"))
sigSrc.setEventHandler { note("\nCtrl-C — stopping…"); done.signal() }
sigSrc.resume()

done.wait()
timer.cancel()
engine?.stop()
engine?.inputNode.removeTap(onBus: 0)
stopProcessTapCapture()
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
note(summary.isEmpty ? "stopped cleanly" : "stopped cleanly — files finalized: " + summary.joined(separator: ", "))
