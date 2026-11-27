# One printed character, two typed forms: the 鎭 and circle rules

Appendix items: 14, 15. Dates: 23–24 November 2026 (JST).

Terms used here:

- A **variant** is a different Unicode character for what is visually almost the same Hanja. 鎭 (U+93AD) and 鎮 (U+93AE) are an example.
- An **editorial default** is a rule the editor applies where the scan is too small to show which form was printed.
- The **locked** text is the transcription frozen as the final original-language edition.

## Summary

The draft text of 9,844 reviewed regions contained 145 occurrences of 鎭 and 36 of 鎮. Both forms appeared even on a single page where the scan shows the same stroke pattern in two names.

The book also uses a small circle in two roles: as the digit zero and as a separator or placeholder. The draft used two Unicode circles, 〇 (U+3007) and ○ (U+25CB), without a consistent rule.

## Impact

The same printed character was typed two ways. Search, comparison and any later identity matching would treat the two forms as different text.

There were 166 disputed circle marks across 163 regions.

## How it was noticed

A count of the draft text showed both forms of 鎭. A comparison of crops at the indexed locations favored 鎭 in the clear examples.

The circle question came up repeatedly in model disagreements, which counted ○ and 〇 as different readings.

## Root cause

OCR and models choose between near-identical code points without seeing a real difference. Small and blurred characters do not show the distinguishing stroke. The circle has two meanings, so no single code point is right everywhere.

## Fix

The maintainer set a source-character rule: confirmed occurrences of the same printed character take one reading, and any different model assignment is a conflict to resolve.

On four scan contact sheets, 鎭 was verified directly in 81 of 181 indexed locations. All 81 showed 鎭. The maintainer then chose 鎭 for the whole edition unless a legible impression shows 鎮. The other 100 locations take 鎭 by that editorial default. The final pass changed 36 characters: 24 supported by direct inspection and 12 by the default. Verified readings and defaults are stored in separate fields, so a reader can tell which is which.

For circles, the maintainer approved 〇 for numeric zero and ○ for separators and name placeholders, each sized to the original ink. Applying the rule changed 85 characters in 84 regions.

On 24 November, while drafting endnotes, at least 12 instances of 〇 were found after 卒 ("died"), where they act as separators. Under the rule they should be ○. The locked text was not changed. A shared endnote records the discrepancy.

## Lesson

Decide variant and symbol policies early, before mass correction, and write them down as editorial rules.

Keep "verified on the scan" separate from "applied by default".

Check the locked text against the rules afterwards. A rule adopted partway through can be contradicted by text that was settled earlier.

## Evidence

- The conversion work log section "Circle encoding and the printed form of 진", and the endnotes draft entry of 24 November.
- The technical workflow record, section 5, on verified characters and editorial defaults.
- The per-occurrence 진 review table and the circle decision table kept with the conversion work.
