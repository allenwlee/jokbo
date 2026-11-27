# The renderer measured its neighbor's ink

Appendix item: 19. Date: 21 November 2026 (JST).

Terms used here:

- The **renderer** draws each character of the reviewed layout into the PDF. To size and place a glyph, it measures the scan's ink inside a small **measuring window** around the character's position.

## Summary

In the closing prose on pp. 135–136, characters sit close together. The renderer's measuring window sometimes covered part of the next character, so it sized or placed a glyph using its neighbor's ink.

## Impact

Glyphs overlapped or crowded each other. A period sat against the last syllable of a sentence. Parentheses looked oversized.

## How it was noticed

A source-to-proof comparison during a screen of rare fallback glyphs showed drift in two adjacent runs. A later spacing screen found 27 closely placed pairs.

## Root cause

A fixed window size assumes clear space between characters. In crowded text the window catches ink from the next glyph.

## Fix

The fix took several proof rounds. Glyph centers were corrected in the reviewed input, windows were narrowed, and glyphs were made smaller where the scan supported it. Vertical parentheses were rotated to match the source and set at 80%.

Each round accepted some adjustments and rejected others that crowded neighboring characters. All 27 pairs from that screen were addressed by the final round of this series. Each build passed the renderer's own checks, and a page-by-page image comparison showed changes only on the two closing-prose openings.

The spelling and punctuation were never changed.

## Lesson

Review fitted placement visually wherever text is dense. Keep rejected trials as well as accepted ones, so the reason for each choice survives.

A screen that finds crowded pairs does not certify the layout. Say what it covered.

## Evidence

- The conversion work log, 21 November entries for the successive afterword placement proofs.
- The technical workflow record, section 6, on measuring windows.
