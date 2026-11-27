# Defects that only a whole-book comparison finds

Appendix items: 18, 20. Dates: 21–23 November 2026 (JST).

Terms used here:

- A **run** is one stretch of positioned text in the layout, usually one column.
- A **proof** is a rendered draft PDF to be checked against the scan.
- An **ink-difference screen** overlays scan and proof and marks ink that appears in one but not the other.

## Summary

Some errors had correct characters in the wrong place, or extra characters from duplicated runs. Character-level checks could not see them.

On p. 86, the date 純廟丁丑一八一七 was drawn across the heading 喆得 (Hangul 철득). Its transcription was correct; its position was not.

On p. 114, the bottom and sides of the inner page border were incomplete.

Two duplicated runs left extra marks. On p. 20, an extra 且 stood after a branch label. On another page, a stroke transcribed as 一 sat over an existing 女.

## Impact

A date drawn over a name makes both hard to read and can suggest the wrong owner for the date. A broken border makes the page look damaged. Duplicate marks add text the book does not contain.

## How it was noticed

The p. 86 and p. 114 defects were found by a whole-book layout comparison on 23 November. It paired every opening, at reduced scale, with a larger strip and an ink-difference screen. All 72 overview pairs were inspected.

The maintainer reported the extra 且 on p. 20, and a similar imperfect inner border on p. 115. The third reading in context identified the two overlapping duplicate runs.

## Root cause

Text checks compare characters. They do not see where a character sits, or that a whole run appears twice. Duplicates came from overlapping runs produced in separate passes.

## Fix

On p. 86, the date's anchor moved 36 source pixels left, which aligns the column with the scan. On p. 114, four continuous rules now follow the source frame. The p. 115 inner frame was rebuilt the same way. Source and corrected crops were compared for each change.

The two duplicate runs were removed after all original run references were processed, so no other reference shifted.

## Lesson

Proof the complete rendered book against the scan, opening by opening, in original order. Record which openings and which strips were actually inspected.

Check placement separately from reading. A page-scale screen does not prove small names and dates, and a character check does not prove placement.

When removing runs, do it last and check that references to other runs are unchanged.

## Evidence

- The conversion work log entries "Whole-book layout comparison — 23 November 2026", "User-reported corrections awaiting final pass" and "Third reading in context".
- The technical workflow record, section "Final digital draft, 23 November 2026".
- The draft open-source plan's note "Proof the complete rendered book against the scan".
