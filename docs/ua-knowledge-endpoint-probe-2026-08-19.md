# UnifyApps Knowledge as a retrieval endpoint — probe record, 2026-08-19

Operator question (2026-08-19): can UnifyApps Knowledge be exposed as an endpoint
with the retriever baked in, so the call-assistant queries it directly, bypasses the
Brain's agentic flow, and reduces dependence on PKMS? Probed by the call-advisor
session from the advisor worktree. Everything below is tagged [verified] (observed
this sitting, command or artifact in hand) or [reported] (operator's word / trace
pasted into chat) or [inferred].

## 1. What exists

- **Public docs [verified, fetched 2026-08-19]:** no documented knowledge-retrieval
  endpoint. Knowledge is agent-bound (Integrate Knowledge Base → Ingestion /
  Settings; "Knowledge Sets" share one corpus across agents). MCP servers and
  "Callable via API" expose *workflows/automations*, not knowledge. The Unify AI
  automation node has 13 actions, none of them search/retrieve.
- **`ReferFromKnowledge` [reported — agent trace pasted by operator]:** a built-in
  agent tool action. Input: `query` only. Output: text blob of `<chunk id="n">`
  blocks with `<metadata>name: …</metadata>`, 8 slots, empties at the tail, plus a
  Text2SQL attempt ("No tables and columns found for SQL formation"). Pure
  retrieval, no synthesis. `executeUsingModel` present → an LLM sits in the path
  (rephrase/rerank). `caseId`/`triggeredByAgentId` bind it to an agent.
- **Pre-made API gateway [verified]:** `https://tool.prod-aps1.unifyapps.com/api-endpoint/AI-FDE-/Refer-from-knowledge`
  — built by the AI-FDE group, wraps an agent whose only job is the knowledge
  binding. Operator observed [reported] the wrapped agent opens **no sessions**
  when hit → the endpoint calls the retrieval stage directly.
  - Contract [verified from schema + 11 live calls]: `POST`, JSON
    `{"query": string}` (`additionalProperties: false`, `query` not even required);
    response `{"response": {"topChunks": [string × 20]}}`, non-streaming. Each chunk
    is a *string* `[content:…, start_line:N, end_line:N, …, embedding_content:…]\n<metadata>appName: github;name: file.md</metadata>`
    — key:value dump, not JSON; `embedding_content` duplicates `content` (≈2× bloat);
    adjacent chunks are overlapping windows of the same file. No scores.
  - **No authentication [verified]:** plain POST, no header, HTTP 200 with full
    chunks. Anyone with the URL reads the FDE corpus. Finding for the endpoint's
    owners; NOT a foundation to build a live dependency on.

## 2. Ranking [verified]

Knowledge source has ranking enabled [reported, operator saw the toggle]. Six
identical-query runs: top 9 chunks identical in identical order every run; 16 of
the 20 common to all six, union 24 — churn only in positions 10–20. Pattern
(exact doc → its implementation JSON → neighbours → one obvious miss at #17) is a
reranked top-20. Slow runs were NOT better: the 2 s and 54 s runs shared 18/20 with
the same top 9. Treat `topChunks` as rank-ordered best-first; no calibrated scores,
so "top N" works, thresholds don't.

## 3. Latency [verified]

| condition | samples | wall-clock |
|---|---|---|
| single-stream, same query | 6 | 9.1 / 54.0 / 11.5 / 14.7 / 5.7 / 2.0 s |
| 5 concurrent, different queries | 10 | 35–87 s for the 5 that returned; **5 timed out at 120 s** |

connect ≈ 40 ms, TLS ≈ 80 ms, firstbyte ≈ total on every run → all time is
server-side before first byte. No warm-up trend (fastest run was the last). Under
concurrency the pipeline serialises/throttles — concurrent "race ×3, first wins"
does NOT help; it slows everything. [inferred] the seconds and the variance live in
the LLM stages (query rephrase, Text2SQL attempt that runs even with no tables,
reranker) plus shared-tenant queueing, not in vector search.

## 4. What the corpus knows [verified, 5 of 10 topic probes returned]

Every hit is `appName: github` — a GitHub-indexed repo of UnifyApps internal
product docs + platform config/code (`uacode configs/platform-features/…`,
connector node JSON, `glossary.md`, `tools-and-actions.md`, `voicebot.md`,
`sap_rfc.md`, learning-byte scenarios with Slack-thread links). It is the FDE
team's platform-assistant corpus: how the product works, down to config paths.

| probe | result |
|---|---|
| LLM providers / BYO model | strong (model library, `ai_agent_llm_model` entity) |
| SAP connector | strong (RFC doc, IDoc trigger/send nodes) |
| HITL / approval | strong ("Require approval" runtime, governance evaluator) |
| voice / telephony | strong (Voicebot, Genesys queues, Voiceflow, VAD) |
| competitors (Workato/MuleSoft/Boomi) | **none** — generic integrations pages only |
| pricing ×2, on-prem/VPC, SOC2/ISO, SLA | **timed out under load — unanswered**. Given the corpus (engineering docs, not sales collateral) pricing/SLA expected absent, deploy/security partial at best. Re-probe one at a time to close. |

Raw responses and the probe script: advisor scratchpad
(`resp1–6.json`, `probe_*.json`, `probe.py` — `python3 probe.py 1 pricing pricing2 deploy security sla`
re-runs the five sequentially). Not committed (third-party corpus text).

## 5. Reading for the track (advisor assessment, not a ruling)

- **Pre-call pack slice: yes.** A knowledge endpoint exists in practice; feed it a
  handful of topic queries before call days, sequentially, ≥ 90 s timeout, keep top
  N (≥ 8, tail jitters), parse `content` + `<metadata>name>` only (the other keys
  are source-type-specific), dedup by `(name, start_line, end_line)`, drop
  `embedding_content`, merge as `pack/ua-slice.json` with its own manifest. Chunks
  carry **no shareability / verified_at** → enter as unlocked, undated; canon stays
  the source for 🔒 and staleness (laws 6/7). Cuts PKMS dependence for
  product-truth, not for pricing, objections, competitive, or client facts.
- **Mid-call automatic hint path: no** (p50 ~10 s, tail ≥ 54 s, worse under load;
  the "nothing slow mid-call" law stands).
- **Operator-triggered "let me check" lookup lane (P1.5 candidate):** legitimate
  as a separate async lane — local pack answers first, UA result arrives when it
  arrives, hard client timeout ~15 s with a graceful "nothing" state. Gated on:
  (a) an **own, authenticated clone** bound to the chosen Knowledge Set — not the
  FDE gateway; (b) a 30+-call latency sample at a realistic hour; (c) a
  **data-processor ruling** — a transcript-derived query is customer speech leaving
  the Mac to UnifyApps (law 1 today names only Anthropic); internal P1 calls
  low-risk, external calls a real posture question.
- **Ask to FDE/product:** not "give us a retrieval endpoint" (exists) but "a
  retrieval-only mode with rephrase + Text2SQL off" — that is where the seconds
  are. Plus: put auth on the gateway.

## 6. Open items created

- Operator: pick the Knowledge Set / agent the call-assistant clone binds to;
  stand up the authed clone. Then advisor writes `scripts/ua-knowledge-query.py`
  + pack-slice merge.
- Operator: finish the five timed-out probes (pricing etc.) one at a time.
- Operator: data-processor ruling (internal calls first) before any in-call use.
- Operator: tell the FDE owners the gateway is unauthenticated.
