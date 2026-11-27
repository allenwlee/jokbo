# Transcription and glyph review

This guide covers getting from a cleaned scan to a reviewed layout: a first machine reading, region geometry, independent readings by vision models, and review of each disputed character against the scan. The figures come from one full book, the 1989 Anseong Lee jokbo of the Jangsu branch (143 page sides in 72 openings). They describe that book and those runs, not general accuracy.

Terms used here:

- **OCR** (optical character recognition): software that turns an image of text into characters. This project used Tesseract.
- **Vision model**: a large language model that accepts images. This project called them through OpenRouter, a service that routes one API to many model providers.
- **Region** or **crop**: a rectangle cut from the scan around one run, with a stable ID.
- **Glyph**: the printed shape of one character.

## 1. Keep page identity fixed first

Before any reading, freeze two files and record their SHA-256:

- the **cleaned spreads PDF**: one PDF page per opening, duplicates removed, in book order;
- the **page map**: one record per page side with its printed page number (or none), its position in book order, its opening, its side, its kind (title, numbered, photo, blank) and the transform from the raw scan to the cleaned page.

`examples/synthetic-book/scan/page-map.json` shows the format. Printed page numbers are missing on some sides of most books, so every later record carries the book-order sequence as well as the printed number. This repository does not include a scan-cleaning tool; any method works as long as it produces these two files and they stay fixed.

## 2. OCR baseline

Run OCR with the right language data and vertical segmentation to get initial text runs and their rectangles. Treat the output as a draft to compare against. OCR errors can be confident, and a model asked to check OCR may miss them.

## 3. Geometry proposals and crop boards

`pilot/convert-to-digital/map_layout.py` (needs OpenCV) proposes text regions and rules from the cleaned pages. On the Lee book it proposed 10,383 text regions and 4,058 rules. These are proposals: a box can join two marks, split a name, or land on the next row.

`pilot/convert-to-digital/prepare_review.py` cuts each layout run from the scan, enlarges it, prints its region ID inside the image, and writes a manifest that maps each ID back to scan coordinates. It also flags crops with almost no ink. On the practice book:

```sh
python pilot/convert-to-digital/prepare_review.py examples/synthetic-book/layout.json \
  --source examples/synthetic-book/scan/spreads.pdf \
  --page-map examples/synthetic-book/scan/page-map.json --output work/review
# 3 openings, 37 regions, 8 source crop boards, 1 crops with almost no scan ink
```

The flagged crop, `S001-L-0013-000`, is the practice book's deliberately misplaced run: its layout position is 150 pixels away from where the scan prints it, so the crop shows blank paper. Check geometry and text separately. On a real chart page in the Lee book, both independent model readers agreed on a reading for a misplaced crop, because both read the neighbouring row that the box had landed on.

## 4. Independent readings

`pilot/convert-to-digital/read_regions.py` sends labelled crop boards to vision models and saves every response by crop ID. It reads `OPENROUTER_API_KEY` from the environment. Default models in the script are `qwen/qwen3-vl-235b-a22b-instruct` and `google/gemini-2.5-flash`. It requests temperature 0, a strict JSON answer keyed by crop ID and at most 1,700 output tokens, runs six workers, retries up to three times, and caches responses by a hash of the request so a rerun does not pay twice. `--model` runs a single model, which gives draft readings only.

The models see the crop, not the draft text. That is the point: an independent reading can disagree with the draft. The crop prompt asks the model to keep Hanja and Hangul exactly as printed, use `?` for unknown characters, and not infer or normalise names.

`pilot/convert-to-digital/parallel_review.py` runs the same reader as separate jobs and merges them. `run` needs an explicit `--max-jobs` and model. That limit counts jobs, not money, and each job can retry three times, so start with a small batch and watch the charges.

What the Lee runs showed:

- **Whole-page passes are a screen, not a review.** Gemini 2.5 Flash-Lite screened all 143 sides for US$0.205 and returned 1,669 findings, capped at 12 per page. It missed all six characters that had been deliberately changed in a pilot opening. In one entry it proposed 1945 where the scan shows 1965.
- **Short crops beat full pages.** On seven selected control crops, Qwen3-VL 235B and Gemini 2.5 Flash each read 7 of 7 and Flash-Lite 5 of 7. The sample was chosen, so it says nothing about whole-book accuracy.
- **One crop per request when scoring.** Prompts with several images sometimes returned correct-looking readings under the wrong crop IDs.
- **Agreement is evidence, not proof.** A third reader (`google/gemini-3-flash-preview`) on 2,503 disputed regions left two readers agreeing on 1,632 and 871 still disputed. Some agreements were both models reading the wrong row.
- **Models invent explanations.** A confident reason attached to a reading is not evidence. Check the scan.

Record for every call: provider, requested and served model ID, settings, prompt or prompt file, reported usage and cost, and whether a human or model made the final decision. Write "not recorded" when a value is missing; do not reconstruct it.

## 5. Glyph review against the scan

The rule that matters most: **establish what the printed character is from the scan before choosing between model answers.**

1. Find clear printings of the disputed character in the same book. Compare stroke by stroke at the crop positions, with the surrounding text, and note the stroke that tells the candidates apart.
2. When the scan shows that several locations hold the same character, bind them all to one Unicode reading. That reading governs the layout, the rendered PDF and the database.
3. Record every model or OCR answer that differs from the verified reading as a **conflict**. This includes two runs of the same model that disagree with each other and two models that agree on the wrong answer. Keep the raw answers and their locations.
4. If a crop is misplaced, blurred or too short to line up, leave that location open. An open reading is a valid result.
5. Reopen a verified reading only on new source evidence, and record why.

Look for a better printing of the same name or word. Names are often printed twice: small in a chart cell or index, and larger in the full entry, sometimes with a Hangul reading. Two Lee examples, both people born before 1921:

- An early draft read `圭氟` in a small chart printing. Qwen and Gemini Flash read `圭氤` on the crop, and the full entry on p. 107, which prints `圭氤` with the Hangul reading 규인, supports it. Flash-Lite read `主氣` on the same crop.
- The larger printing of `㦥燮` on p. 38, with its Hangul reading 헌섭, shows the 忄 radical and settled `㦥` over `幰` where a small index printing was unclear.

Headings need the same care. On printed p. 1 the OCR replaced the last character of the preface heading with a Hangul syllable. On p. 4 it misread two characters of the generation-chart heading, and the full-page model caught only one of them.

Short strokes and circles drop out. Isolated readers often lose the horizontal strokes in numerals such as `一一一`, so read references in the full row and follow them to the entry they point to. The practice book includes `一一一` on its index page and both circle forms, `〇` (U+3007, a zero in dates) and `○` (U+25CB, a mark); `database/test_synthetic_book.py` checks that they survive transcription and rendering. A circle can be a number, a separator or a name placeholder, so record its role and encode it by role.

For disputes that the glyph alone cannot settle, use the context questions in [editorial review](editorial-review.md).

## 6. Recording decisions

`pilot/convert-to-digital/review_ledger.py` keeps findings and decisions in one JSON ledger tied to the scan, page map and layout hashes. `add` records a finding, `decide` attaches an editorial decision, and `import-review` merges a revision-matched `parallel_review.py merge` result; imported disagreements stay pending. None of these commands changes the layout. `apply_corrections.py` writes a new layout and ledger into a new directory once an editor has chosen a replacement, after checking the old layout hash, opening, run, expected text and decision. It never edits the original and never applies pending findings.

The ledger's `bootstrap` command needs a single-page cleaned PDF named in the page map (`clean_pdf`). The practice book does not include one, so the quickstart does not run the ledger.

Verified readings are stored per location (`verified_source_characters`, offsets counted from zero within the region). Editorial defaults are stored separately (`editorial_default_characters`); a verified reading at the same location wins.
