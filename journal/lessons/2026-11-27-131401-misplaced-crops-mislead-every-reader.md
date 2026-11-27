# A misplaced crop makes every reader wrong in the same way

Appendix items: 1, 12. Dates: 20–23 November 2026 (JST).

Terms used here:

- A **region** is a box that the layout step proposed around one line or cell of printed text.
- A **crop** is the small image cut from the scan inside that box. The vision models only saw crops, not the whole page.
- **Source-layout pixels** are pixel positions on the cleaned scan, which is the reference image for all coordinates.

## Summary

Two reading errors came from the boxes, not from the readers.

On printed p. 16, a quick-reference chart page, the boxes for one column sat one grid row too high. Both independent models read the row next to the intended one, and they agreed with each other.

Separately, four region boxes cut through the lower character of 見下 ("see below", a cross-reference marker). The model kept answering 見, because the 下 was mostly outside its crop.

## Impact

Agreement between two models looked like confirmation, but both answers described the wrong row.

On a genealogy chart, the row decides which generation and which family a name belongs to. A row error can therefore turn into a wrong relationship later.

On p. 16, 34 reviewed cells were affected. Without the fix, the chart positions would have been wrong in the assembled book.

Dropping 下 removes the direction of a cross-reference.

## How it was noticed

For p. 16, an expanded-context reread of the 59 regions that the models had marked unreadable left 20 still uncertain. Seventeen of those 20 were on p. 16. Looking at one of the crops showed the target box sitting above the printed character. A side-by-side detail of scan and proof then showed the column one grid row above its scan position, even though the grid lines themselves aligned.

For 見下, a deliberately selected sample of 32 flagged regions was checked at crop scale. Several crops showed the 下 cut off. An eight-region follow-up drew a red rectangle on a larger crop and showed the original box cutting through 下.

## Root cause

The boxes are proposals made by image processing. Some p. 16 boxes came from an early pilot layout that did not locate that text reliably. A crop reader reads only what is inside its box, so it reads the wrong place faithfully.

## Fix

The 34 reviewed p. 16 entries were moved down 63 source-layout pixels. Their horizontal positions and the chart rules stayed as they were. An earlier positional review had already moved nine name runs on the same page down by 57–63 pixels. In that review, Qwen read all nine corrected crops as expected and Gemini matched seven.

For 見下, enlarging the target box by 12 source-layout pixels vertically produced 見下 in all four cases. The wider box did not fix every case. In one test the model dropped a zero circle, and in another it returned only two of three digits. A wider box can also pull in neighboring text.

No model reading was applied automatically. The corrections went through the editorial review and the final assembly.

## Lesson

Check geometry and text as two separate questions. A correct reading of the wrong box is still wrong.

Keep the crop ID printed inside each image and keep coordinates back to the scan. Then any reading can be traced to the exact pixels the model saw.

When a reading looks wrong, look at the box before blaming the model.

Treat agreement between models as a candidate for review, not as proof.

## Evidence

- The conversion work log: the 20 November positional review of pp. 16–17, the 23 November "independent sample and crop-boundary test" entries, and the third reading in context.
- The technical workflow record, section "Final digital draft, 23 November 2026", which records the 63-pixel move.
- The notes collected in the draft open-source plan, which name the p. 16 case as the example for checking geometry and text separately.
