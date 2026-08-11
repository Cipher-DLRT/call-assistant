// P1 streaming STT helper — adapted from spike/stt_bench/bench_whispercpp.c
// (check (c) winner: whisper.cpp, HOP 1.0 / WIN 10.0, greedy, single segment).
// One instance per audio stream. Clock = samples received, so wav replay and
// live capture behave identically.
//
//   stt-stream <model.bin> --stdin            # raw s16le mono 16k PCM on stdin
//   stt-stream <model.bin> --replay <wav>     # 16k mono s16 wav, real-time paced
//
// Output: one JSON line per hop on stdout:
//   {"t": <window_end_s>, "rms_db": <hop rms dBFS>, "text": "..."}
// Diagnostics on stderr. Exits 0 on EOF.

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <ggml-backend.h>
#include <whisper.h>

#define HOP 1.0
#define WIN 10.0
#define RATE 16000
#define HOP_N ((long)(HOP * RATE))
#define WIN_N ((long)(WIN * RATE))

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

static float *read_wav_16k_mono(const char *path, long *n_out) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    char id[4]; uint32_t sz, riff_type;
    if (fread(id, 1, 4, f) != 4 || memcmp(id, "RIFF", 4) ||
        fread(&sz, 4, 1, f) != 1 || fread(&riff_type, 4, 1, f) != 1) { fclose(f); return NULL; }
    int16_t *pcm = NULL; long n = 0;
    while (fread(id, 1, 4, f) == 4 && fread(&sz, 4, 1, f) == 1) {
        if (!memcmp(id, "data", 4)) {
            pcm = malloc(sz);
            if (!pcm || fread(pcm, 1, sz, f) != sz) { free(pcm); fclose(f); return NULL; }
            n = sz / 2;
            break;
        }
        fseek(f, sz + (sz & 1), SEEK_CUR);
    }
    fclose(f);
    if (!pcm) return NULL;
    float *out = malloc(n * sizeof(float));
    for (long i = 0; i < n; i++) out[i] = pcm[i] / 32768.0f;
    free(pcm);
    *n_out = n;
    return out;
}

// escape for a JSON string: ", \, and control chars
static void json_escape(const char *src, char *dst, size_t dst_sz) {
    size_t j = 0;
    for (const char *p = src; *p && j + 3 < dst_sz; p++) {
        unsigned char c = (unsigned char)*p;
        if (c == '"' || c == '\\') { dst[j++] = '\\'; dst[j++] = c; }
        else if (c < 0x20) dst[j++] = ' ';
        else dst[j++] = c;
    }
    dst[j] = 0;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s model.bin --stdin | --replay wav\n", argv[0]);
        return 1;
    }
    setvbuf(stdout, NULL, _IOLBF, 0);

    int replay = !strcmp(argv[2], "--replay");
    if (!replay && strcmp(argv[2], "--stdin")) { fprintf(stderr, "bad mode\n"); return 1; }

    float *wav = NULL; long wav_n = 0, wav_pos = 0;
    if (replay) {
        if (argc < 4) { fprintf(stderr, "--replay needs a wav\n"); return 1; }
        wav = read_wav_16k_mono(argv[3], &wav_n);
        if (!wav) { fprintf(stderr, "bad wav\n"); return 1; }
    }

    ggml_backend_load_all();  // Homebrew ggml gotcha: backends live in libexec
    double t0 = now_s();
    struct whisper_context_params cparams = whisper_context_default_params();
    struct whisper_context *ctx = whisper_init_from_file_with_params(argv[1], cparams);
    if (!ctx) { fprintf(stderr, "model load failed\n"); return 1; }
    fprintf(stderr, "model load: %.2fs\n", now_s() - t0);

    struct whisper_full_params wp = whisper_full_default_params(WHISPER_SAMPLING_GREEDY);
    wp.language = "en";
    wp.translate = false;
    wp.no_context = true;
    wp.no_timestamps = true;
    wp.single_segment = true;
    wp.print_progress = false;
    wp.print_realtime = false;
    wp.print_special = false;
    wp.print_timestamps = false;

    // warmup (Metal shader compile), before any output
    float silence[RATE] = {0};
    t0 = now_s();
    whisper_full(ctx, wp, silence, RATE);
    fprintf(stderr, "warmup decode: %.2fs\n", now_s() - t0);

    float ring[WIN_N];              // last WIN seconds
    long filled = 0;                // valid samples in ring (<= WIN_N)
    long total = 0;                 // samples received overall
    int16_t hop_i16[HOP_N];
    float hop_f[HOP_N];
    double start = now_s();

    for (;;) {
        // acquire one hop of samples
        long got = 0;
        if (replay) {
            got = wav_n - wav_pos < HOP_N ? wav_n - wav_pos : HOP_N;
            if (got <= 0) break;
            memcpy(hop_f, wav + wav_pos, got * sizeof(float));
            wav_pos += got;
            // real-time pacing: don't emit hop k before wall time k*HOP
            double due = start + (double)(total + got) / RATE;
            double dt = due - now_s();
            if (dt > 0) usleep((useconds_t)(dt * 1e6));
        } else {
            got = (long)fread(hop_i16, sizeof(int16_t), HOP_N, stdin);
            if (got <= 0) break;
            for (long i = 0; i < got; i++) hop_f[i] = hop_i16[i] / 32768.0f;
        }
        total += got;

        // hop RMS in dBFS
        double acc = 0;
        for (long i = 0; i < got; i++) acc += (double)hop_f[i] * hop_f[i];
        double rms = sqrt(acc / got);
        double rms_db = 20.0 * log10(rms > 1e-9 ? rms : 1e-9);

        // append to ring (shift-left window; WIN_N is small)
        if (filled + got > WIN_N) {
            long drop = filled + got - WIN_N;
            memmove(ring, ring + drop, (filled - drop) * sizeof(float));
            filled -= drop;
        }
        memcpy(ring + filled, hop_f, got * sizeof(float));
        filled += got;

        whisper_full(ctx, wp, ring, (int)filled);
        char text[4096] = "";
        for (int s = 0; s < whisper_full_n_segments(ctx); s++)
            strlcat(text, whisper_full_get_segment_text(ctx, s), sizeof(text));
        char esc[8192];
        json_escape(text, esc, sizeof(esc));
        printf("{\"t\": %.1f, \"rms_db\": %.1f, \"text\": \"%s\"}\n",
               (double)total / RATE, rms_db, esc);
    }

    whisper_free(ctx);
    return 0;
}
