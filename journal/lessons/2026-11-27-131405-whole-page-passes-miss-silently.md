# A whole-page pass can return nothing, or miss what you planted

Appendix items: 6, 8. Dates: 20 and 24 November 2026 (JST).

Terms used here:

- **OCR** (optical character recognition) is software that turns an image of text into characters. Tesseract produced this project's first OCR draft.
- A **planted error** is a character changed on purpose in a test copy, so you know the right answer in advance.
- An **opening** is a pair of facing pages as the book lies open.

## Summary

Model passes that looked at whole pages missed things without saying so.

Gemini 2.5 Flash-Lite audited the OCR of all 143 page sides. It missed all six characters deliberately changed in the pilot pages.

A Qwen3-VL 235B full-page comparison on 12 sample pages returned locatable findings for only one page. It missed two heading corrections that focused crop reading had already found: one character in the preface title on p. 1, and two in a branch-chart heading on p. 4.

On 24 November, one Qwen3-VL request returned zero people for an opening with clearly visible names.

## Impact

An empty or short answer looks like "nothing to fix".

On one page, Flash-Lite proposed 1945 where the scan shows 1965. Accepting it would have changed a year by twenty years.

Flash-Lite also proposed readings for a blank page side, from faint text showing through the paper.

## How it was noticed

The planted errors gave a known answer to check against. Without them, the misses would have been invisible.

The heading corrections had already been found by focused crop reading, so the full-page result could be compared.

The zero-person result was compared with the page image, which plainly shows names.

## Root cause

At full-page scale, small Hanja are a few pixels wide. The audit prompt also capped findings at 12 per page, and models tend to confuse nearby text. An answer with no findings carries no information about what the model actually examined.

## Fix

Whole-page output became a review queue, never an accepted correction.

Reading moved to short, labeled crops. On seven selected control crops, Qwen3-VL 235B and Gemini 2.5 Flash each read 7 of 7 and Flash-Lite read 5 of 7. The controls were chosen on purpose, so this is not a book-wide accuracy rate.

No model-generated people from the person calibration were imported.

## Lesson

Plant known errors in a test copy before trusting any automatic pass. Score the pass on them first.

Treat "zero results" as a result that needs checking, not as a clean page.

Use full-page passes to find candidates. Use tight crops for readings.

## Evidence

- The character audit, "Results" and "What the full-book screen measured".
- The technical workflow record, section 2, on the 1945/1965 proposal and the blank side.
- The run record for the person-appearance candidate stage, which records the zero-person request with its model, provider, time and cost.
