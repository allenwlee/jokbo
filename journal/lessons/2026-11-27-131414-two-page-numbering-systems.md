# A chronological page number is not a printed page number

Appendix item: 27. Date: 24 November 2026 (JST).

Terms used here:

- The **printed page number** (folio) is the number printed on the page. Some pages, such as the title and photo plates, have none.
- The **chronological page number** counts every page side from the start of the book, numbered or not.

## Summary

A test in the split-name stage failed at first. It used a chronological page ID where the stored value was a printed page number.

## Impact

Small, because the test caught it. The same mistake in a query or an import would have attached text to the wrong page.

## How it was noticed

The test failed before the successful run.

## Root cause

The project uses two page numbering systems for good reasons. Both are plain integers, so nothing stops one being used in place of the other.

## Fix

The test was corrected to use the actual stored page ID. Nine tests then passed.

## Lesson

Keep both numbers, and name them so they cannot be confused, for example `printed_page_number` and `book_page_sequence`. Write at least one test where the two differ.

## Evidence

- The run record for the split name candidate pass.
- The technical workflow record, "Source and page identity", which describes the page map.
