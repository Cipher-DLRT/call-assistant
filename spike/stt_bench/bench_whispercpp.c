// P0 check (c): whisper.cpp streaming-partial latency harness.
// Implements the metric in docs/runbook-p0c-stt-speed.md: real-time-paced
// sliding window (hop 1 s, window <= 10 s), latency = emit_time - T_window_end.
// Usage: bench_whispercpp <model.bin> <wav 16k mono s16> <out.csv> [max_seconds]

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

static int cmp_d(const void *a, const void *b) {
    double d = *(const double *)a - *(const double *)b;
    return d < 0 ? -1 : d > 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s model wav out.csv [max_s]\n", argv[0]); return 1; }
    setvbuf(stdout, NULL, _IONBF, 0);

    long n = 0;
    float *audio = read_wav_16k_mono(argv[2], &n);
    if (!audio) { fprintf(stderr, "bad wav\n"); return 1; }
    double total = (double)n / RATE;
    if (argc > 4) { double m = atof(argv[4]); if (m > 0 && m < total) total = m; }

    ggml_backend_load_all();  // discover Metal/CPU backend modules (libexec)
    double t0 = now_s();
    struct whisper_context_params cparams = whisper_context_default_params();
    struct whisper_context *ctx = whisper_init_from_file_with_params(argv[1], cparams);
    if (!ctx) { fprintf(stderr, "model load failed\n"); return 1; }
    printf("model load: %.2fs\n", now_s() - t0);

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

    // warmup (Metal shader compile etc.), excluded from measurement
    t0 = now_s();
    whisper_full(ctx, wp, audio, RATE);
    printf("warmup decode (1 s audio): %.2fs\n", now_s() - t0);

    FILE *csv = fopen(argv[3], "w");
    fprintf(csv, "T,latency_s,text\n");
    double lats[4096]; int n_lat = 0;

    double start = now_s();
    double last_end = 0;
    while (last_end < total) {
        double elapsed = now_s() - start;
        double T = floor(elapsed / HOP) * HOP;
        if (T > total) T = total;
        if (T <= last_end) {
            double next = start + last_end + HOP;
            double dt = next - now_s();
            if (dt > 0) usleep((useconds_t)(dt * 1e6));
            continue;
        }
        long i0 = (long)(fmax(0, T - WIN) * RATE);
        long i1 = (long)(T * RATE);
        if (i1 > n) i1 = n;
        whisper_full(ctx, wp, audio + i0, (int)(i1 - i0));
        double lat = (now_s() - start) - T;

        char text[4096] = "";
        for (int s = 0; s < whisper_full_n_segments(ctx); s++)
            strlcat(text, whisper_full_get_segment_text(ctx, s), sizeof(text));
        for (char *p = text; *p; p++) if (*p == '"') *p = '\'';
        fprintf(csv, "%.1f,%.3f,\"%s\"\n", T, lat, text);
        printf("T=%4.1fs  lat=%.3fs\n", T, lat);
        lats[n_lat++] = lat;
        last_end = T;
    }
    fclose(csv);

    qsort(lats, n_lat, sizeof(double), cmp_d);
    printf("partials: %d  p50: %.3fs  p90: %.3fs\n",
           n_lat, lats[n_lat / 2], lats[(int)(0.9 * (n_lat - 1))]);
    whisper_free(ctx);
    return 0;
}
