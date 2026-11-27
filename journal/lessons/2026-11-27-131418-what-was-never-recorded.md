# What was never recorded

Appendix items: 28, 29, 30, 35. Dates: 20–24 November 2026 (JST).

Terms used here:

- A **run record** is a short document written for each stage: what ran, on what inputs, with which models, at what cost, and what was checked.
- A **receipt** is a machine-readable file that records exact inputs, outputs, fingerprints, counts and times.
- `ce-compound` is a coding-assistant skill that asks, at the end of a stage, whether a durable lesson should be written down.
- A **baseline** is the starting result that later work is compared with.

## Summary

Four kinds of information were not captured when the work happened.

1. **A stage with no run record at the time (item 28).** The SQLite layout foundation stage on 24 November ran without `ce-compound` and without timings. Its run record was reconstructed afterwards, at about 21:07 JST, from saved files and session output. The start and end times and per-step runtimes are unknown. The working database's file time, 20:56 JST, is not a measured runtime.
2. **The OCR baseline (item 29).** Tesseract produced the first text using traditional-Chinese and Korean language data and vertical page segmentation. The exact command, version, confidence thresholds and the count of uncertain characters were never recorded.
3. **The coding assistant itself (item 30).** In several stages, the assistant's model, version, reasoning setting, token use and cost were not captured. This includes the in-session vision readings in the first pilot and the interactive agent review in the database stages.
4. **Time spent (item 35).** The first 60-opening proof has a file time of 18:30 on 20 November. Proof 243 has 08:19 on 21 November. That is about 14 hours of elapsed work across many model calls, reviews, corrections and rebuilds. No record shows how that time divided between them.

## Impact

The OCR baseline cannot be reproduced exactly.

The total cost of the project is unknown. Recorded model charges are listed in [costs and models](../costs-and-models.md), but the coding assistant's usage, which did much of the work, is missing.

Nobody can say from the records which steps were slow, so there is no evidence for where parallel work would help.

## How it was noticed

Writing later run records and the reproducibility notes exposed each gap. The project's own rule for run records requires models, settings and timings, and these stages could not supply them.

## Root cause

The first stages were exploration, and recording was not built into the tools. Interactive assistant sessions do not produce a usage receipt by default. File times are easy to mistake for measurements.

## Fix

Later stages wrote a run record and a receipt for each run, with exact Japan-time start and end times, input and output fingerprints, models, providers, settings and reported charges. The whole-book edition's provider report has the time, cost and model for every pass.

The reconstructed record is labeled as a reconstruction, and it says what it cannot establish.

The gaps are published here and in the costs file as gaps. Nothing was estimated to fill them.

## Lesson

Decide what each stage must record before it starts: command, software versions, models and providers, settings, start and end times, and cost. Write it to a receipt automatically.

Record the assistant's own model and usage too, if your tools allow it. If they do not, say so in the run record.

Instrument long sessions with timestamps per step. Before recommending parallel work, measure quality, time, retries and cost against a fixed sequential sample.

## Evidence

- The retrospective run record for the SQLite layout foundation.
- The technical workflow record, sections 1 (OCR baseline) and 7 (timing).
- The run records for the embedded-name, person-candidate, grouping and page-extraction stages, each of which states what agent usage was unavailable.
- The draft open-source plan's note on testing parallel review.
