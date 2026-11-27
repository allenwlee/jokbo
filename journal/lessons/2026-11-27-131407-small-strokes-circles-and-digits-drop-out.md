# Small strokes, circles and digits drop out

Appendix items: 10, 11, 13. Dates: 20–23 November 2026 (JST).

Terms used here:

- The book writes numbers with Hanja numerals. 一, 二 and 三 are one, two and three horizontal strokes. A page reference such as 一一一 (111) is three separate single strokes.
- 〇 is a circle used as zero.
- A **generation label** is the column text at the edge of a chart page that says which generation each row is.
- A **screen** is an automatic check that lists candidates for a person to inspect. It does not correct anything by itself.

## Summary

Readers, both models and people, kept losing the smallest marks.

Crop readers that saw one index cell at a time dropped horizontal strokes in references made of 一, 二 and 三. Later, during manual reconstruction, separate 一 strokes were wrongly merged into 二 or 三. All 51 reconstructed three-digit references were rechecked against enlarged crops and corrected. A later stroke-count screen still found five more errors on four pages.

A right-edge strip review of all 120 page sides found a missing 一 in one generation label on p. 18. A later screen of isolated ink found two more missing 一 in generation labels on p. 20. The strip review had missed them.

In a sample of flagged regions, models dropped zero circles and digits. On p. 43 the name 相默, printed with the reading 상묵, was read as 상무.

## Impact

A wrong page reference sends a reader to the wrong family. A missing stroke in a generation label puts a whole row in the wrong generation. A dropped final consonant changes a name.

## How it was noticed

Comparing isolated cell reads with readings of the full chart row recovered strokes the cell readers had skipped.

Following a reference to its target page, and checking that the target points back, exposed misread digits. One example: a reference printed as two separately spaced 一 strokes followed by a third numeral had been typed as 二 plus that numeral.

Stroke-count screens, strip comparisons and isolated-ink screens each found cases the earlier checks missed.

For 상묵, the larger printing of 默 and the printed final ㄱ in the Hangul settled the reading.

## Root cause

Single strokes and small circles are a few pixels high. When a crop is tight, a stroke near its edge can be lost. When strokes are evenly spaced, two separate 一 look like one 二. Models also tend to drop a final consonant toward a more common syllable.

## Fix

Index references were read from full rows. That restored 122 printed references on pp. 12–15.

References were checked in both directions against the pages they point to. Stroke-count screens were run on three-numeral references and then on mixed two- and three-numeral references.

Hanja names were paired with nearby Hangul readings and compared with the Unicode Unihan reference readings. That screen paired 940 names and flagged 44. All 44 were inspected and one clear transcription error was found. A reference reading never overrides what the book prints.

When a name was unclear, the reader followed the index to the full entry, where the name is printed larger. For example, the full entry for 㦥燮, with its Hangul reading 헌섭, on p. 38 resolved a rare character.

## Lesson

Read numbers and labels in their full row or column, not as isolated cells.

Follow every page reference to its target and check that it points back.

Run several narrow screens, each for one kind of mark. Record what each screen covers and what it cannot see. None of them is an accuracy rate.

Each check found errors the previous check missed. Plan for that rather than declaring a page clean after one pass.

## Evidence

- The conversion work log: the 20 November review of the final 60 openings, and the 21 November checkpoint entries on stroke-count, strip and isolated-ink screens, reference checks and the name-reading screen.
- The conversion work log, 23 November follow-up sections on the flagged sample and on Hangul names.
- The draft open-source plan's notes on isolated cell reads versus full rows, and its "Pass 3" table.
