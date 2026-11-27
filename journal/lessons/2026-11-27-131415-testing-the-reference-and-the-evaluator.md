# Testing the reference set and the evaluator

Appendix items: 22, 23. Date: 24 November 2026 (JST).

Terms used here:

- A **reference set** is a small set of entries checked by hand against the scan. It is the expected answer.
- An **evaluator** is the script that compares the program's output with the reference set and scores it.
- A **holdout** is a reference case prepared before looking at the program's output on it, so it can test the program fairly.

## Summary

Evaluating the first grouping trial against the reference set showed two mistakes in the reference itself. In one case the Korean reading was ordered wrongly after the name heading. In another, a text run that continues a grave description was assigned to the wrong place.

An independent read-only review of the evaluator found four problems. It discarded character offsets. It treated a continuation fragment's extra cross-page material as an error. It ignored the order of source runs. And the run record still carried an outdated in-progress statement.

## Impact

A wrong reference makes a correct program look wrong, or a wrong one look right. An evaluator that ignores offsets and order can score a partly wrong group as exact.

## How it was noticed

The reference errors appeared when the trial's disagreements were checked against the source layout. The evaluator problems were found by a separate review that read the code and the reference.

## Root cause

The reference was prepared quickly from pilot material and had not been checked against the layout for every run. The evaluator compared run membership, not exact text slices.

## Fix

The reference was corrected by checking the source layout, not by declaring the program right. Version 1 is kept in history. Because the correction was made after seeing the trial, the revised cases are no longer a blind test. A new holdout was prepared on another page before any predictions for it were inspected. On it, the middle entry and both partial passages had the expected slices in order.

The evaluator now compares exact slices and their order. It labels a covered continuation `fragment_covered` and allows extra slices around a continuation. New tests cover partial slices, reverse order and an extra slice on a different opening. All 13 tests passed after the fixes.

## Lesson

Test the test. When an evaluation disagrees, check the reference against the source before changing either side.

Once you have corrected a reference after seeing results, it is no longer independent. Keep a separate holdout.

Have someone other than the author review the evaluator.

## Evidence

- The run record for the geometric grouping trial (the first evaluation and the revised reference).
- The run record for reference expansion, section "Review and correction".
- The expanded entry-grouping reference review notes.
