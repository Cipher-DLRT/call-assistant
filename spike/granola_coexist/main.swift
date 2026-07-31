// P0 check (a): can ScreenCaptureKit tap system audio while Granola records
// the same audio simultaneously?
//
// Captures system audio for N seconds (default 30, override with first arg),
// prints a per-second level meter, and writes out.wav into the current
// directory. Run it while a video is playing and Granola is recording; the
// check passes only if BOTH this tool's wav AND Granola's transcript contain
// the video audio. Runbook: docs/runbook-p0a-granola-coexist.md

import Foundation
import AVFoundation
import ScreenCaptureKit

setvbuf(stdout, nil, _IONBF, 0)

let seconds = CommandLine.arguments.count > 1 ? (Int(CommandLine.arguments[1]) ?? 30) : 30
let outURL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
    .appendingPathComponent("out.wav")

final class Tap: NSObject, SCStreamOutput, SCStreamDelegate {
    var file: AVAudioFile?
    var framesThisSecond = 0
    var sumSquaresThisSecond: Float = 0
    var second = 0
    var peakDb: Float = -1000
    var nonSilentSeconds = 0
    var failed: String?
    let done = DispatchSemaphore(value: 0)

    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer,
                of type: SCStreamOutputType) {
        guard type == .audio,
              let desc = CMSampleBufferGetFormatDescription(sampleBuffer),
              let asbd = CMAudioFormatDescriptionGetStreamBasicDescription(desc),
              let format = AVAudioFormat(streamDescription: asbd) else { return }
        let frames = CMSampleBufferGetNumSamples(sampleBuffer)
        guard frames > 0,
              let pcm = AVAudioPCMBuffer(pcmFormat: format,
                                         frameCapacity: AVAudioFrameCount(frames)) else { return }
        pcm.frameLength = AVAudioFrameCount(frames)
        guard CMSampleBufferCopyPCMDataIntoAudioBufferList(
            sampleBuffer, at: 0, frameCount: Int32(frames),
            into: pcm.mutableAudioBufferList) == noErr else { return }

        if file == nil {
            do {
                file = try AVAudioFile(forWriting: outURL, settings: format.settings)
                print("capture started: \(Int(format.sampleRate)) Hz, \(format.channelCount) ch")
            } catch {
                failed = "cannot write \(outURL.path): \(error.localizedDescription)"
                done.signal()
                return
            }
        }
        try? file?.write(from: pcm)

        guard let data = pcm.floatChannelData else { return }
        let n = Int(pcm.frameLength)
        var sum: Float = 0
        for ch in 0..<Int(format.channelCount) {
            for i in 0..<n { let v = data[ch][i]; sum += v * v }
        }
        sumSquaresThisSecond += sum / Float(format.channelCount)
        framesThisSecond += n
        if framesThisSecond >= Int(format.sampleRate) {
            second += 1
            let rms = (sumSquaresThisSecond / Float(framesThisSecond)).squareRoot()
            let db = 20 * log10(max(rms, 1e-9))
            peakDb = max(peakDb, db)
            let sound = db > -50
            if sound { nonSilentSeconds += 1 }
            print(String(format: "t+%02ds  %6.1f dBFS  %@", second, db, sound ? "SOUND" : "silent"))
            framesThisSecond = 0
            sumSquaresThisSecond = 0
            if second >= seconds { done.signal() }
        }
    }

    func stream(_ stream: SCStream, didStopWithError error: Error) {
        failed = "stream stopped: \(error.localizedDescription)"
        done.signal()
    }
}

let tap = Tap()
let queue = DispatchQueue(label: "audio-tap")
var streamRef: SCStream?

Task {
    do {
        let content = try await SCShareableContent.excludingDesktopWindows(
            false, onScreenWindowsOnly: true)
        guard let display = content.displays.first else {
            tap.failed = "no display found"
            tap.done.signal()
            return
        }
        let filter = SCContentFilter(display: display, excludingWindows: [])
        let cfg = SCStreamConfiguration()
        cfg.capturesAudio = true
        cfg.excludesCurrentProcessAudio = true
        cfg.sampleRate = 48000
        cfg.channelCount = 2
        cfg.width = 64
        cfg.height = 64
        cfg.minimumFrameInterval = CMTime(value: 1, timescale: 1)
        let stream = SCStream(filter: filter, configuration: cfg, delegate: tap)
        streamRef = stream
        try stream.addStreamOutput(tap, type: .audio, sampleHandlerQueue: queue)
        try await stream.startCapture()
        print("recording system audio for \(seconds) s — keep the video playing…")
    } catch {
        tap.failed = "could not start capture: \(error.localizedDescription)"
        tap.done.signal()
    }
}

tap.done.wait()
let stopSem = DispatchSemaphore(value: 0)
Task {
    try? await streamRef?.stopCapture()
    stopSem.signal()
}
stopSem.wait()
queue.sync { tap.file = nil }  // finalize the wav header before exiting

if let f = tap.failed {
    print("CAPTURE FAILED: \(f)")
    print("If this mentions permission: System Settings → Privacy & Security → " +
          "Screen & System Audio Recording → enable your terminal app, then re-run.")
    exit(1)
}
print(String(format: "done: %d/%d seconds had sound, peak %.1f dBFS",
             tap.nonSilentSeconds, tap.second, tap.peakDb))
print("wav written to \(outURL.path) — play it back to confirm the video audio is there")
exit(tap.nonSilentSeconds > 0 ? 0 : 2)
