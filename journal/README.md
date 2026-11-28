# Project journal

This journal records how one family's printed genealogy was turned into a searchable digital edition and a database, between 18 and 25 November 2026. It lists every stage, the models and services used, what they cost, and every documented mistake: how it was found, what it affected and what fixed it.

The book is the 1989 Anseong Lee genealogy (jokbo, 족보) of the Jangsu branch. It is a printed volume of 137 numbered pages, set mostly in Hanja (Chinese characters used in Korean writing) with some Hangul (the Korean alphabet). Most of it is family charts, read top to bottom and right to left.

The journal is for two kinds of reader: a person or family planning to digitize their own genealogy, and an AI agent doing that work for them. If you are starting a similar project, read the lessons before you start. Most of them cost little to prevent and a lot to find later.

All times are Japan Standard Time (JST, UTC+9).

## How to read this journal

- The [stage log](#stage-log) below is in date order. Each day links to the lessons that came out of it.
- Each [lesson](lessons/) follows the same shape: Summary, Impact, How it was noticed, Root cause, Fix, Lesson, Evidence. This is a "blameless" format: it describes what the process allowed to happen, not who made the mistake.
- [Costs and models](costs-and-models.md) lists every recorded model, provider, cost and timing, and every gap where nothing was recorded.
- The [coverage table](#coverage-of-the-36-documented-mistakes) maps each of the 36 documented mistakes and challenges to its lesson.

The Evidence section of each lesson names the internal records it draws on, such as "the conversion work log" or "the run record for the grouping trial". Those records stay in the project's private repository, because they contain family data. The figures in this journal are copied from them.

### Privacy in this journal

People born in 1920 or earlier appear here in full, with names and page numbers. Anyone else, including anyone whose birth year is missing or not yet verified, appears only as a short glyph or reading needed to explain a lesson, with no page number, date or relatives. Counts and costs include everyone, but no figure points to one such person. The person who ran this project is called "the maintainer" throughout.

## Stage log

### 18 November: research and planning

- Researched how Korean family and state records could be used to check the genealogy. Checked a family tradition against the Goryeosa, the official history of the Goryeo dynasty, and recorded the clan's modern census ranking.
- Saved the scanned book and an English translation of its prose sections in the project repository. Saving the scan in the repository's history is where the [publishing lesson](lessons/2026-11-27-131423-publishing-without-leaking.md) begins.
- Drafted the database plan: one permanent identity for each person, a source location for every fact, and an English PDF that keeps the book's original page order and charts. Start with three sample openings (pairs of facing pages) before the whole book.
- Models and costs: not recorded.

### 18–20 November: six-page pilot

The commits do not date this work exactly.

- Built English and bilingual pilot PDFs and a small SQLite database (eight tables) for six printed pages in three openings. The pilot held 73 person records.
- Tesseract OCR (optical character recognition) produced the first text. An attempted OpenAI `gpt-5-mini` reading failed with an "insufficient credits" error. Follow-up readings were done by the coding assistant looking at images in the conversation. Later vision calls went through OpenRouter.
- Lessons: [provider failures](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md), [what was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md).

### 20 November: renderer, page audit and the 60-opening review

- 14:22: added a reusable renderer that turns a reviewed layout file into a searchable PDF, with a made-up example layout.
- 15:09: started the draft plan for an open-source release, and began collecting notes for it.
- Audited the OCR of all 143 page sides with Gemini 2.5 Flash-Lite, recovering 16 failed responses with Gemini 2.5 Flash. Cost US$0.205. The audit missed all six characters planted as a test.
- Mapped the page geometry: 10,383 candidate text regions and 4,058 candidate ruled lines across 72 openings.
- First Qwen3-VL 235B crop-reading pass on 61 openings: US$0.512. A second, independent reading of the final 60 openings: US$0.572. A third-reading adjudication of 2,503 disputed regions with `google/gemini-3-flash-preview`: US$1.257.
- 18:30: first 60-opening proof. The session ran overnight.
- Lessons: [whole-page passes](lessons/2026-11-27-131405-whole-page-passes-miss-silently.md), [multi-image prompts](lessons/2026-11-27-131406-multi-image-prompts-swap-crop-ids.md), [misplaced crops](lessons/2026-11-27-131401-misplaced-crops-mislead-every-reader.md), [small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md).

### 21 November: screens, placement and the physical book

- 08:19: proof 243, about 14 hours after the first proof. No breakdown of that time exists.
- Ran narrow checks one after another: stroke counts in page references, the right-edge generation labels, isolated ink, cycle-year dates, and Hanja names against their Hangul readings. Each found errors the earlier checks had missed.
- Found that the PDF's hidden search layer makes text extraction return some characters twice.
- Fixed crowded glyphs in the closing prose across several proofs.
- Two model rereads of one blurred character invented explanations. The maintainer then checked the printed book for the readings no scan could settle.
- 15:15: saved the research and conversion work.
- Lessons: [small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md), [PDF text layers](lessons/2026-11-27-131410-pdf-double-text-layer.md), [renderer window](lessons/2026-11-27-131412-renderer-measuring-window.md), [invented explanations](lessons/2026-11-27-131409-models-invent-explanations.md), [the physical book](lessons/2026-11-27-131422-the-physical-book-settles-what-scans-cannot.md), [what was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md).

### 22 November

No work is recorded for this day.

### 23 November: review tooling, the full crop pass and the final draft

- 10:11: planned the review tooling. A review ledger (one record per finding, with its evidence) imported 2,903 findings.
- Tried parallel workers and three ways of reaching Qwen3-VL (OpenRouter automatic routing, OpenRouter pinned to DeepInfra, DeepInfra directly). All trial costs were below one US cent each.
- Read every region of the book once: 1,708 crop boards, 9,844 regions. Gemini 2.5 Flash-Lite hit rate limits after 312 boards and Qwen3-VL read the rest. Cost US$0.583.
- Tested crop boundaries on a sample, reread the 59 unreadable regions, and reread all 2,074 disagreements with wider crops (US$0.193).
- The maintainer set editorial rules for the 鎭/鎮 variant and for the two uses of the circle mark.
- A third, in-context reading of the 475 remaining disagreements settled 455 from the scan, with no model calls. The maintainer supplied readings for 16 of the 20 left open.
- Rebuilt the digital draft (72 openings, 15 editorial notes), compared every opening with the scan, fixed the reversed fallback font order and the oversized notes font. The maintainer designated the result as the final original-language edition.
- 15:17 and 23:15: saved the review workflow and the reviewed draft.
- Lessons: [provider failures](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md), [misplaced crops](lessons/2026-11-27-131401-misplaced-crops-mislead-every-reader.md), [small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md), [variant and circle rules](lessons/2026-11-27-131408-variant-and-circle-rules.md), [whole-book proofing](lessons/2026-11-27-131411-whole-book-proofing-and-duplicate-runs.md), [fonts](lessons/2026-11-27-131402-font-order-and-font-embedding.md), [the physical book](lessons/2026-11-27-131422-the-physical-book-settles-what-scans-cannot.md).

### 24 November: endnotes, archives and the database

- Chose the endnote marker and drafted 480 endnotes with 926 links. Found that the circle rule was contradicted by text already locked.
- Found full-size household-register images behind an archive catalog's thumbnails.
- Built the SQLite layout foundation from the locked edition: 72 openings, 143 page records, 9,842 text runs, no people yet. Its run record was reconstructed afterwards.
- Calibrated person extraction with eight model requests (US$0.087). The answers passed every substring check and were still wrong about who was a person. None was imported.
- Created 1,190 person candidates with fixed rules, then 421 more from spouse and father phrases: 1,611 unreviewed appearances.
- Hand-mapped one sample page, built a small reference set, and grouped chart entries by measured ruled lines. The reference set and its evaluator both had errors.
- Tested page-level extraction on six pages and tightened the importer.
- 21:57–22:18: whole-book database edition. 686 requests, US$3.068. Result: 3,349 source-located appearance dossiers, 4,732 fact claims and 1,580 relationship claims, all marked as proposals. An offline replay reproduced the database byte for byte.
- 21:50–22:21: saved each database stage and published the edition internally.
- Lessons: [variant and circle rules](lessons/2026-11-27-131408-variant-and-circle-rules.md), [archive thumbnails](lessons/2026-11-27-131419-archive-thumbnails.md), [what was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md), [source-matched text](lessons/2026-11-27-131404-source-matched-text-is-not-a-person.md), [whole-page passes](lessons/2026-11-27-131405-whole-page-passes-miss-silently.md), [testing the reference](lessons/2026-11-27-131415-testing-the-reference-and-the-evaluator.md), [code review scope](lessons/2026-11-27-131416-code-review-scope.md), [two page numbers](lessons/2026-11-27-131414-two-page-numbering-systems.md), [grouping trial](lessons/2026-11-27-131413-grouping-trial-crash-and-skipped-pages.md), [person ID scope](lessons/2026-11-27-131417-reader-person-id-scope.md), [provider failures](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md).

### 25 November: why the record begins in 1592

- Researched why the book's dated entries begin with Lee Saeng (李笙), born in 1592, the year the Imjin War began. Turned the research into a narrated, map-animated short video in English and Korean.
- Narration used OpenAI `gpt-4o-mini-tts`, checked by transcribing it back with `whisper-1`. Frames were drawn locally with Pillow and joined with `ffmpeg`. Narration in both languages cost "well under one US dollar"; the exact figure was not recorded.
- 17:45: saved the research and the video pipeline.
- Lessons: [text-to-speech](lessons/2026-11-27-131420-text-to-speech-pronunciation.md), [video pipeline paths](lessons/2026-11-27-131421-video-pipeline-hard-coded-paths.md).

### After the log: preparing this public repository

On 27 November, planning for this public repository found several ways family data could leak, starting with the scans saved in the working repository's history. That stage has its own lesson: [publishing without leaking](lessons/2026-11-27-131423-publishing-without-leaking.md).

### 28 November: auditing dates in the database

- A query for birth years found nine fact records with three-digit years, such as 0958. Every one is a four-digit year in the book. The 一 was lost at a column, gutter or page break, or skipped by the reader in mid-column. The same audit found deaths stored as births and dates attached to generation labels.
- Added the date checks, the column join and a golden set of the checked cases. The database records themselves were not yet corrected.
- Lesson: [years lose their leading 一](lessons/2026-11-28-221257-years-lose-their-leading-one.md).

## Coverage of the 36 documented mistakes

Every mistake and challenge documented in the project's records maps to one lesson. Some lessons cover several items that share a cause.

| # | Mistake or challenge | Lesson |
|---:|---|---|
| 1 | A p. 16 crop was misplaced by one grid row; both independent readers read the adjacent row; 34 entries moved down 63 px | [Misplaced crops](lessons/2026-11-27-131401-misplaced-crops-mislead-every-reader.md) |
| 2 | Fallback font order reversed in the 23 November final-pass build (32 characters, 383 occurrences) | [Fonts](lessons/2026-11-27-131402-font-order-and-font-embedding.md) |
| 3 | The notes assembly embedded the whole Arial Unicode font; subsetting cut the PDF from 23.6 MB to 8.4 MB | [Fonts](lessons/2026-11-27-131402-font-order-and-font-embedding.md) |
| 4 | OpenAI `gpt-5-mini` returned insufficient credits; switched to in-session vision, then OpenRouter | [Provider failures](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md) |
| 5 | Exact-substring validation passed with zero errors while courtesy names, index names and Hanja/Hangul pairs were counted as separate people | [Source-matched text](lessons/2026-11-27-131404-source-matched-text-is-not-a-person.md) |
| 6 | Qwen3-VL returned zero people on an opening with visible names | [Whole-page passes](lessons/2026-11-27-131405-whole-page-passes-miss-silently.md) |
| 7 | Multi-image prompts returned valid characters under the wrong crop IDs | [Multi-image prompts](lessons/2026-11-27-131406-multi-image-prompts-swap-crop-ids.md) |
| 8 | Full-page Flash-Lite missed all six planted characters; a Qwen full-page pass missed heading corrections | [Whole-page passes](lessons/2026-11-27-131405-whole-page-passes-miss-silently.md) |
| 9 | Sixteen page-audit responses timed out or failed to parse; recovered with Gemini 2.5 Flash | [Provider failures](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md) |
| 10 | Cell readers dropped strokes in 一/二/三 references; 51 references rechecked, 5 more errors found later | [Small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md) |
| 11 | Missing 一 in generation labels on pp. 18 and 20, missed by an earlier screen | [Small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md) |
| 12 | A region rectangle cut through 下, so the model kept reading 見 | [Misplaced crops](lessons/2026-11-27-131401-misplaced-crops-mislead-every-reader.md) |
| 13 | Models dropped zero circles and digits; 상묵 was read as 상무 | [Small strokes](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md) |
| 14 | 鎭/鎮 inconsistency (145 vs 36, both forms on one page) led to an editorial rule | [Variant and circle rules](lessons/2026-11-27-131408-variant-and-circle-rules.md) |
| 15 | The circle convention was contradicted by at least 12 locked occurrences | [Variant and circle rules](lessons/2026-11-27-131408-variant-and-circle-rules.md) |
| 16 | Model explanations invented component analyses for disputed glyphs | [Invented explanations](lessons/2026-11-27-131409-models-invent-explanations.md) |
| 17 | The PDF's double text layer made extraction return a character twice | [PDF text layers](lessons/2026-11-27-131410-pdf-double-text-layer.md) |
| 18 | A date drawn across a heading on p. 86 and an incomplete border on p. 114, found only by whole-book proofing | [Whole-book proofing](lessons/2026-11-27-131411-whole-book-proofing-and-duplicate-runs.md) |
| 19 | The renderer's measuring window caught neighboring ink; crowded pairs needed repeated fixes | [Renderer window](lessons/2026-11-27-131412-renderer-measuring-window.md) |
| 20 | Duplicate runs left an extra 且 and a stray 一 in the render | [Whole-book proofing](lessons/2026-11-27-131411-whole-book-proofing-and-duplicate-runs.md) |
| 21 | The first grouping trial crashed; 27 pages were skipped for poor line detection | [Grouping trial](lessons/2026-11-27-131413-grouping-trial-crash-and-skipped-pages.md) |
| 22 | The reference set itself had two errors, found by evaluating against it | [Testing the reference](lessons/2026-11-27-131415-testing-the-reference-and-the-evaluator.md) |
| 23 | An independent review found the evaluator discarded offsets, ignored run order and mis-scored continuations | [Testing the reference](lessons/2026-11-27-131415-testing-the-reference-and-the-evaluator.md) |
| 24 | A code-review skill run failed because its scope included unrelated unstaged files | [Code review scope](lessons/2026-11-27-131416-code-review-scope.md) |
| 25 | Page extraction: 17 quote alignment failures, 7 facts crossing entry boundaries, a label defect, 2 of 10 parent choices wrong on a sample page | [Source-matched text](lessons/2026-11-27-131404-source-matched-text-is-not-a-person.md) |
| 26 | A second reader reused a local person ID with a different cited run | [Person ID scope](lessons/2026-11-27-131417-reader-person-id-scope.md) |
| 27 | A test confused a chronological page number with a printed page number | [Two page numbers](lessons/2026-11-27-131414-two-page-numbering-systems.md) |
| 28 | A stage ran without `ce-compound` or timings and was reconstructed afterwards | [What was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md) |
| 29 | The Tesseract command, version and thresholds were never recorded | [What was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md) |
| 30 | The coding assistant's model, version, tokens and cost were not captured in several stages | [What was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md) |
| 31 | An archive catalog image was only a 100 × 150 thumbnail | [Archive thumbnails](lessons/2026-11-27-131419-archive-thumbnails.md) |
| 32 | Text-to-speech mispronounced a place name; a transcribe-back check with retries was added | [Text-to-speech](lessons/2026-11-27-131420-text-to-speech-pronunciation.md) |
| 33 | The video pipeline was hard-wired to `/tmp` paths and copy-pasted retry scripts | [Video pipeline paths](lessons/2026-11-27-131421-video-pipeline-hard-coded-paths.md) |
| 34 | Checks against the physical book settled scan ambiguities that no model could | [The physical book](lessons/2026-11-27-131422-the-physical-book-settles-what-scans-cannot.md) |
| 35 | A 14-hour, 60-opening session had no instrumented time breakdown | [What was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md) |
| 36 | Nine dates had three-digit years: the 一 was lost at column and page breaks or skipped by the reader; some were also stored as births or on the wrong appearance | [Leading 一](lessons/2026-11-28-221257-years-lose-their-leading-one.md) |
| — | Publishing stage: leak risks found while planning this repository | [Publishing without leaking](lessons/2026-11-27-131423-publishing-without-leaking.md) |

## All lessons

1. [A misplaced crop makes every reader wrong in the same way](lessons/2026-11-27-131401-misplaced-crops-mislead-every-reader.md) (items 1, 12)
2. [Font order and font embedding in the final build](lessons/2026-11-27-131402-font-order-and-font-embedding.md) (items 2, 3)
3. [Provider failures: credits, timeouts and rate limits](lessons/2026-11-27-131403-provider-failures-and-fallbacks.md) (items 4, 9)
4. [Text that matches the source can still mean the wrong thing](lessons/2026-11-27-131404-source-matched-text-is-not-a-person.md) (items 5, 25)
5. [A whole-page pass can return nothing, or miss what you planted](lessons/2026-11-27-131405-whole-page-passes-miss-silently.md) (items 6, 8)
6. [Multi-image prompts put right answers under wrong IDs](lessons/2026-11-27-131406-multi-image-prompts-swap-crop-ids.md) (item 7)
7. [Small strokes, circles and digits drop out](lessons/2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md) (items 10, 11, 13)
8. [One printed character, two typed forms: the 鎭 and circle rules](lessons/2026-11-27-131408-variant-and-circle-rules.md) (items 14, 15)
9. [Model explanations can be invented](lessons/2026-11-27-131409-models-invent-explanations.md) (item 16)
10. [A PDF with two text layers returns characters twice](lessons/2026-11-27-131410-pdf-double-text-layer.md) (item 17)
11. [Defects that only a whole-book comparison finds](lessons/2026-11-27-131411-whole-book-proofing-and-duplicate-runs.md) (items 18, 20)
12. [The renderer measured its neighbor's ink](lessons/2026-11-27-131412-renderer-measuring-window.md) (item 19)
13. [The first grouping trial crashed, then skipped 27 pages](lessons/2026-11-27-131413-grouping-trial-crash-and-skipped-pages.md) (item 21)
14. [A chronological page number is not a printed page number](lessons/2026-11-27-131414-two-page-numbering-systems.md) (item 27)
15. [Testing the reference set and the evaluator](lessons/2026-11-27-131415-testing-the-reference-and-the-evaluator.md) (items 22, 23)
16. [An automated code review failed because its scope was too wide](lessons/2026-11-27-131416-code-review-scope.md) (item 24)
17. [A second reader reused a person ID for a different place](lessons/2026-11-27-131417-reader-person-id-scope.md) (item 26)
18. [What was never recorded](lessons/2026-11-27-131418-what-was-never-recorded.md) (items 28, 29, 30, 35)
19. [An archive catalog image was only a thumbnail](lessons/2026-11-27-131419-archive-thumbnails.md) (item 31)
20. [Text-to-speech mispronounced a place name](lessons/2026-11-27-131420-text-to-speech-pronunciation.md) (item 32)
21. [The video pipeline was tied to one machine](lessons/2026-11-27-131421-video-pipeline-hard-coded-paths.md) (item 33)
22. [The physical book settled what no scan or model could](lessons/2026-11-27-131422-the-physical-book-settles-what-scans-cannot.md) (item 34)
23. [Publishing the methods without publishing the family](lessons/2026-11-27-131423-publishing-without-leaking.md) (publishing stage)
24. [Years lose their leading 一](lessons/2026-11-28-221257-years-lose-their-leading-one.md) (item 36)
