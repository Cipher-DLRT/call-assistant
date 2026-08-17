# p2-pack-automation-plan.md — DRAFT v1 (2026-08-12)

> Drafted in the call-assistant chat while P1 shadow calls accumulate. **Build starts
> only on P1 EXIT** (three graded calls, bars met: ≥98 channel-split, ≥90 voiceprint,
> operator precision bar). Gate state at draft: D4 (dossier rendered per-account md)
> DONE — operator-reported 2026-08-12, VERIFY AT SOURCE at build start (read the
> actual md, don't trust this line). This plan crosses two tracks and defines their
> contract; the dossier chat reviews the EQ14 half, the call-assistant chat owns the
> Mac half.

## 1. What P2 adds (from CLAUDE.md v1.2)

Calendar-triggered pre-call packs (canon + per-account dossier slice) · pkms_reads
wiring (law 3's deferral ends) · "pack ready" Telegram card · first external-call
use (separate operator ruling at the end, not implied by the build).

## 2. The pack bundle contract (the cross-track interface — versioned)

`pack-bundle.v1/` per meeting: `canon.json` + `manifest.json` (as today, A1
manifest law) + `account.md` (the dossier slice for the mapped account) +
`meeting.json` (event id, title, time, attendees, account, internal|external
flag). The Mac loop loads the bundle whole; absence of account.md = generic pack
(today's behavior), never an error. Contract changes bump the version; both
tracks pin to it.

## 3. EQ14 side (dossier-track build; n8n, reflex-plane pattern)

- Calendar watcher flow: upcoming meetings window (next 24 h, work hours);
  attendee-domain → account mapping (new small table, seeded from the dossier's
  account list — TBV at build: authoritative account list location).
- Pack build job per meeting: canon export (status='active', manifest — the SAME
  script/law as the Mac's manual export, moved on-box) + dossier md slice for the
  account + meeting.json → staged under a per-meeting directory on EQ14.
- Telegram card: "pack ready — <meeting> <account>" (existing card patterns;
  (chat_id, message_id) stored for refresh per standing note).
- NO new ingress: EQ14 serves nothing new. Staging directory is read via the
  operator's existing ssh path only.

## 4. Mac side (call-assistant build)

- Pull, never push-to-Mac: a launchd timer (work hours, every 15 min) + a pull on
  menu-bar Start Shadow fetches staged bundles over the EXISTING ssh loopback
  path (outbound-only law; evaluated and rejected: a Tailscale Serve endpoint on
  EQ14 — new ingress for no gain at one consumer).
- Menu bar gains: bundle picker when multiple upcoming meetings have packs
  (default = nearest by start time); status line shows which account's pack is
  loaded.
- Loop change: retrieval reads bundle canon; hint prompt gains the account.md
  slice as context (prompt version bump → hint-v2, graded before/after per the
  standing prompt-versioning practice).

## 5. pkms_reads wiring (the enumerated deferred write)

Per-call artifact already logs which fact_ids each hint cited. Post-call, the
stop path ships the read log as a JSON batch over the same ssh loopback; the
insert executes ON-BOX via psql as the enumerated retrieval-path writer. The Mac
still holds no Postgres credential (law 9 intact — the ssh path is the operator's
existing one). Failure mode: ship-later queue on the Mac; reads are analytics,
never blocking.

## 6. Acceptance (run-keyed, both halves)

Fixture calendar event (internal, mapped account) → watcher stages a bundle with
correct account.md + meeting.json → Mac pull lands it → Start Shadow loads it,
status shows the account, retrieval count matches manifest → post-call read batch
appears in pkms_reads with the run key → Telegram card fired once. External-flag
event → pack stages but the loop REFUSES Start unless the external-use ruling
env is set (the P2 gate made structural). Zero residue; live canon untouched
throughout (hash check).

## 7. Sequence

P1 exit declared (call-assistant chat, on graded sheets) → this plan reviewed:
EQ14 half by the dossier chat, contract + Mac half already owned here → fold →
build EQ14 half (dossier Code session) ∥ build Mac half (call-assistant Code
session) against the v1 contract → joint acceptance (§6) → external-call use
remains a SEPARATE operator ruling.

## 8. Open items (named, not blocking the draft)

Account-mapping source of truth (TBV at build) · dossier md slice size budget
(whole file vs sections — decide on the real D4 md, not assumptions) · read-batch
cadence if calls end offline · whether the account.md slice is shareability-safe
by construction (dossier content is internal-only — hints citing it must render
🔒 by default; confirm in review).
