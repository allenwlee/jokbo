# Font order and font embedding in the final build

Appendix items: 2, 3. Date: 23 November 2026 (JST).

Terms used here:

- A **fallback font** supplies a character that the main font does not contain. The edition uses UnGungseo first, then Source Han Serif KR, then Arial Unicode MS.
- **Subsetting** a font means embedding only the characters a PDF actually uses, instead of the whole font file.

## Summary

Two font mistakes were made in the 23 November builds.

The first final-pass build put Arial Unicode MS before Source Han Serif KR. That reversed the fallback order chosen in the earlier font tests.

The step that added editorial notes embedded the whole Arial Unicode font. The book pages themselves were already subset; the notes were not.

## Impact

With the reversed order, 32 distinct characters, in 383 places, were drawn in Arial instead of Source Han. The Unicode values stayed the same, so search and copy were unaffected. The printed shapes did not match the chosen design.

The full Arial embedding made the PDF 23,621,527 bytes. After subsetting it was 8,442,673 bytes.

## How it was noticed

The fallback order was caught by comparing the final-pass build settings with the order recorded in the earlier font tests and in the draft open-source plan.

The records give the before-and-after sizes for the embedding fix. They do not say what prompted the size check.

## Root cause

The font order was set separately in the final-pass build instead of being read from one shared setting.

The notes were assembled by a different step from the book renderer. That step did not reuse the renderer's subsetting.

## Fix

A new build restored the chosen order: Source Han Serif KR first, Arial Unicode MS second. Extracted text, page labels and annotation counts matched the preceding draft on all 73 PDF pages. Three openings were checked visually, including the generation chart and the repaired double borders. The rebuilt PDF was 7,860,161 bytes. The older render receipts still record the order those builds actually used.

The notes assembly now subsets its font from the actual note text, opening labels, identifiers and punctuation. The earlier and the smaller output have identical extracted text, page labels and annotation counts. Rendered samples of four openings and the notes page were pixel-identical. The font coverage check still runs against the complete font before subsetting.

## Lesson

Keep the font order in one configuration that every build step reads.

Record the fallback order actually used in each build's receipt, so a later reader can tell which build used which order.

Subset every font in every part of the PDF. Measure the file before and after, and compare extracted text and rendered pages to show nothing else changed.

## Evidence

- The conversion work log entry "Fallback font order reconciled — 23 November 2026".
- The technical workflow record, section "Final digital draft, 23 November 2026", including the subsetting paragraph.
- The draft open-source plan's notes "Subset fonts in every part of the PDF" and the font order note.
