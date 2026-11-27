# The first grouping trial crashed, then skipped 27 pages

Appendix item: 21. Date: 24 November 2026 (JST).

Terms used here:

- **Grouping** means deciding which text runs on a chart page belong to one person's entry. The trial used the page's ruled lines to find chart rows.
- An **anchor** is the heading (usually a name) that an entry's other text attaches to.

## Summary

The first grouping attempt crashed. Two candidate headings competed to be assigned to the same anchor, and one of them was that anchor itself.

The next attempt ran. It skipped 27 printed pages because it could not detect enough ruled lines on them.

## Impact

The crashed attempt removed its incomplete output and wrote no receipt. Its exact time was not recorded.

Skipping a page is safer than guessing, but it left 27 pages ungrouped.

## How it was noticed

The program stopped with an error. The successful run's receipt listed all 27 skipped pages.

## Root cause

The allocation step did not say that a heading belongs to itself first. Line detection relied on the digital layout's lines, which were incomplete on some pages.

## Fix

The allocation was changed so a heading first belongs to itself.

For line detection, the final pass measured the ink in twelve horizontal bands across each expected chart rule on the cleaned page image. All 588 internal rules on printed pp. 17–134 had support from at least six bands. The result has 1,206 heading groups and 164 row fragments. For 145 fragments, the preceding page has a heading on the matching row; those are stored as possible continuations, not as facts.

No model call was used in this stage.

## Lesson

When a heuristic cannot decide, make it skip and list what it skipped. Then fix the measurement rather than the guess.

Measure the physical page when derived data, such as detected lines, is incomplete.

Record the time and outcome of failed attempts too.

## Evidence

- The run record for the geometric grouping trial, including its "Completed grouping stage" section and its machine-readable receipts.
