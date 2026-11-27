# Costs, models and timings, as recorded

This file lists every model, provider, cost and timing that the project's records state, from 18 to 25 November 2026. All times are Japan Standard Time (JST, UTC+9). Amounts are the charges the providers reported, in US dollars, copied as written.

It also lists what was never recorded. A gap is shown as a gap. Nothing here is estimated to fill one.

Terms used here:

- **OpenRouter** is a service that sends requests to many models and providers through one interface. Most vision calls went through it.
- A **provider** is the company that actually ran the model, for example Google AI Studio, Parasail, Venice or DeepInfra.
- A **request** is one call to a model. A **pass** is a batch of requests with one purpose.
- **Tokens** are the units models count text in. Output limits below are maximum output tokens per request.

## Summary

| What | Recorded amount |
|---|---:|
| Whole-book database edition, 24 November, 686 requests | US$3.06831111 |
| All other recorded model charges, 20–24 November | about US$3.48 |
| Listed amounts added together | about US$6.55 |
| History video narration, both languages, 25 November | "well under one US dollar" (exact figure not recorded) |
| Coding assistant usage, all stages | not recorded |

The added total is only a rough figure. Some passes share calls or retries, so the records warn against adding their amounts without reconciling them. The total also leaves out everything in the "never recorded" section below, including the coding assistant, which did much of the work.

## 20–21 November: OCR, page audit and the first readings

| Pass | Model and provider | Scope | Cost | Notes |
|---|---|---|---:|---|
| First pilot OCR | Tesseract, traditional-Chinese and Korean data, vertical segmentation | Pilot pages, then the numbered pages | none (local) | Command, version and thresholds not recorded |
| Attempted pilot reading | OpenAI Responses API, `gpt-5-mini` | Pilot | none recorded | Failed: insufficient credits |
| Pilot follow-up readings | In-session vision by the coding assistant | Pilot | not recorded | Model, version and usage not recorded |
| Full-page OCR audit | Gemini 2.5 Flash-Lite via OpenRouter; Gemini 2.5 Flash recovered 16 failed responses | 143 page sides | US$0.2052055 | Request identifiers span about 5.6 minutes on 20 November |
| Audit plus model comparisons | Same, plus Qwen3-VL 235B and Gemini 2.5 Flash on seven control crops | As above | US$0.2421974 | Includes the audit's own US$0.2052055 |
| First crop-reading pass | Qwen3-VL 235B via OpenRouter | 61 openings | US$0.5120192 | 8,876 readings, 104 unreadable |
| Second reading, final 60 openings | Not stated beside the figure | 60 openings | US$0.572 | From the conversion work log |
| Third-reading adjudication | `google/gemini-3-flash-preview` | 2,503 disputed regions | US$1.257195 | From its saved review file |
| Focused rereads of single difficult characters | Qwen and Gemini via OpenRouter | A few characters | not stated in the work log | Raw responses kept with the evidence |

Settings of the saved crop-reading script (`read_regions.py`): default models `qwen/qwen3-vl-235b-a22b-instruct` and `google/gemini-2.5-flash`; temperature 0; at most 1,700 output tokens; a strict JSON schema keyed by crop ID; `provider.require_parameters=true`; reasoning disabled for Google models; six worker threads; 80-second timeout; up to three attempts with waits of 1, 2 and 4 seconds. These are the script's settings. The records do not show that every exploratory call used them.

The 60-opening review session ran from about 18:30 on 20 November to 08:19 on 21 November, roughly 14 hours, judged from file times. No breakdown of that time was recorded.

## 23 November: review tooling, provider trials and the full crop pass

| Pass | Model and provider | Scope | Time | Cost |
|---|---|---|---:|---:|
| Tooling trial, sequential | Gemini 2.5 Flash-Lite | 4 jobs, 2 crop boards | 8.126 s | US$0.000223 |
| Tooling trial, two workers | Gemini 2.5 Flash-Lite | 4 jobs | 5.389 s | US$0.00013903 |
| Bounded comparison, sequential | Gemini 2.5 Flash-Lite | 6 boards | 21.297 s | US$0.000667 |
| Bounded comparison, six workers | Gemini 2.5 Flash-Lite | 6 boards: 2 succeeded, 4 rate-limited | 8.006 s | US$0.00013976 |
| Provider trial, automatic routing | Qwen3-VL 235B via OpenRouter, served by Parasail (4) and Venice (2) | 6 boards, 5 workers | 6.954 s | US$0.0024163 |
| Provider trial, pinned | Qwen3-VL 235B via OpenRouter, pinned to DeepInfra | 6 boards | 17.033 s | US$0.00154968 |
| Provider trial, direct | Qwen3-VL 235B, DeepInfra API directly | 6 boards | 42.806 s | estimated US$0.00154968 |
| Full crop-reading pass | Gemini 2.5 Flash-Lite via OpenRouter (Google AI Studio) for 312 boards; Qwen3-VL 235B via OpenRouter automatic routing for 1,396 boards | 1,708 boards, 9,844 regions, 72 openings | not recorded | US$0.58348393 |
| Second-model sample | Gemini 2.5 Flash and Qwen3-VL, each rereading the other's boards | 32 flagged boards | not recorded | US$0.01389002 |
| Unreadable regions, wider crops | Second model family | 59 regions | not recorded | US$0.00452971 |
| Wider-context pass on all disagreements | Other model family via OpenRouter, five concurrent requests | 2,074 regions | not recorded | US$0.19321179 |
| Third reading in context | No model; editorial review of the scans | 475 regions | not recorded | US$0 |

The trials had a US$1 spending target written down in advance. The runner did not enforce a dollar ceiling. The direct DeepInfra figure is an estimate, not a reported charge, and is left out of the totals above.

## 24 November: database stages

| Stage | Model and provider | Requests | Cost | Timing |
|---|---|---:|---:|---|
| SQLite layout foundation | None | 0 | US$0 | Not recorded; reconstructed afterwards |
| Person calibration | Qwen3-VL 235B-A22B Instruct, served by Parasail | 1 | US$0.00197403 | 9.674 s |
| Person calibration | Gemini 2.5 Flash, served by Google AI Studio | 7 | in the total below | in individual receipts |
| Person calibration, total | | 8 | US$0.08662933 | |
| Rule-based candidates, embedded names, split names, sample page, reference expansion, grouping | None | 0 | US$0 | Exact times in each receipt; the sample page insertion took 0.232 s and the split-name pass 0.239 s |
| Exploratory single-page extraction | not stated beside the figure | not stated | US$0.0100667 | Outside the edition total. One run record calls it a reading of chronological page 75, another an experiment on page 69; the records do not reconcile this |
| Six-page extraction trial | `google/gemini-2.5-flash` via OpenRouter, Google AI Studio; temperature 0; reasoning disabled; 22,000 output tokens; concurrency 5 | 6 | per-packet charges in the archived packets; no total in the run record | JST start and end in each packet |
| Validation replay | None | 0 | US$0 | In its receipts |

Calibration settings: temperature 0 and a 6,000-token output limit. For Qwen, reasoning was not specified. For Gemini, reasoning was requested disabled.

### The whole-book database edition

Every pass used `google/gemini-2.5-flash` through OpenRouter, served by Google AI Studio, at temperature 0 with reasoning requested disabled. The first reading allowed 22,000 output tokens with five concurrent workers. The second reading allowed 16,000. Focused candidate reviews allowed 2,000 tokens, gap reviews 12,000 and source-only dossier reviews 5,000. The six calibration responses were reused, so 137 first readings were new requests.

| Pass | Packets | Requests | Cost | Start (JST) | End (JST) |
|---|---:|---:|---:|---|---|
| First reading | 143 | 143 | US$1.2193098 | 21:57:32 | 22:06:33 |
| Page audit | 143 | 143 | US$0.88772944 | 22:02:06 | 22:08:01 |
| Page audit retry | 28 | 28 | US$0.13473934 | 22:04:35 | 22:08:14 |
| Page audit, last retry | 4 | 4 | US$0.01506223 | 22:06:00 | 22:06:54 |
| Appearance reviews | 56 | 56 | US$0.0378217 | 22:10:12 | 22:10:34 |
| Gap reviews | 143 | 216 | US$0.6596170 | 22:11:47 | 22:15:35 |
| Sparse reviews | 84 | 84 | US$0.1102265 | 22:17:12 | 22:17:59 |
| Sparse follow-up | 12 | 12 | US$0.0038051 | 22:18:28 | 22:18:32 |
| **Total** | | **686** | **US$3.06831111** | 21:57:32 | 22:18:32 |

The final assembly ran from 22:18:48 to 22:18:57. Served model weight revisions and the models' private reasoning were not available.

## 25 November: history video

| Step | Tool | Cost |
|---|---|---|
| Narration | OpenAI `gpt-4o-mini-tts`, voice `cedar`, one recording per scene | "well under one US dollar" for one full narration in both languages, including transcription checks |
| Transcribe-back check and word timing | OpenAI `whisper-1` | included above |
| Voice comparison | Four OpenAI and four MiniMax voices | not recorded |
| Frames and video | Python with Pillow, then `ffmpeg`, run locally | none |

## Never recorded

- **The coding assistant.** Its model, served version, reasoning setting, token use and cost were not captured in any stage. The 24 November records say a Codex agent chose methods, made editorial decisions and ran checks. Its usage was unavailable.
- **Tesseract.** The exact command, version, confidence thresholds and the number of uncertain OCR characters.
- **The 18 November research and prose translation.** The records consulted for this journal do not state which tools or models were used, or their cost.
- **The SQLite layout foundation stage.** Start time, end time and per-step runtimes.
- **The first grouping attempt.** Its time. It crashed and wrote no receipt.
- **The reference expansion.** End time and elapsed time.
- **The 60-opening review session.** Any breakdown of the roughly 14 hours between model calls, review, correction and rebuilding.
- **Served model weights.** OpenRouter reports the model name and provider, not the exact weights the provider ran.
- **The full request body** for the first person-calibration requests. The prompt and run list were kept and can be rebuilt; the exact request was not.

## Sources

- The conversion work log and the technical workflow record for 20–23 November.
- The character audit for 20 November.
- The run records for each 24 November stage, and the whole-book run record.
- The edition's provider cost report and assembly receipt.
- The history video folder's README.
