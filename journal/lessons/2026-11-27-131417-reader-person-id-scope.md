# A second reader reused a person ID for a different place

Appendix item: 26. Date: 24 November 2026 (JST).

Terms used here:

- A **local ID** is a short label, such as `p` or `h`, that a model uses within one page answer to attach facts and relatives to the names it found.
- A **foreign-key check** is a database check that every reference points to a record that exists.

## Summary

Each page was read twice. The second reader corrected the first. On one page, a proposed correction used the same local ID and the same name as the first reader, but cited a different text run.

## Impact

Applying the second reader's changes through the first reader's ID map could quietly give a birth or a spouse to a different person. A foreign-key check would accept the result, because both people exist in the database.

## How it was noticed

Comparing the cited source locations of the two readers showed the same ID pointing at different runs. A name comparison alone could not tell whether this was a repeated appearance, a wrong citation or a real correction.

## Root cause

Local IDs are only meaningful inside one answer. Treating them as shared across two answers assumes the readers numbered the page the same way.

## Fix

Both responses and their cited positions are kept. Each reader's claims are attached through that reader's own ID mapping. Ambiguous pairs stay as separate appearances, and the competing assignments are listed for review.

## Lesson

Scope every model-assigned identifier to the answer that produced it. Match on the cited source location before applying a correction that reuses an ID.

When reporting completeness, count pages read, appearances with dossiers, and open identity questions separately. Every database person can be correctly linked to the source while the number of distinct historical people is still unknown.

## Evidence

- The internal solution note "Preserve the scope of each reader's person identifiers".
- The whole-book run record, section "Compound outcome".
