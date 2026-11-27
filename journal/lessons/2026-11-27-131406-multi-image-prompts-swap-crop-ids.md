# Multi-image prompts put right answers under wrong IDs

Appendix item: 7. Date: 20 November 2026 (JST).

Terms used here:

- A **crop ID** is the label that ties each small image to one region of the scan.
- A **contact sheet** (or crop board) is one image holding several labeled crops in a grid.

## Summary

Some early prompts sent several separate crop images in one request. The model returned real, plausible characters, but under the wrong crop IDs.

## Impact

Each reading looked valid on its own. Matched to the wrong ID, it would have written a correct character into the wrong place in the book.

## How it was noticed

Comparing answers with the crops they claimed to describe showed the swaps.

## Root cause

Nothing in the separate images tied each image to its ID except their order in the request. The model did not keep that order reliably.

## Fix

The scored focused tests used one crop per request.

The later crop-reading script prints each crop's label inside the image itself, on a contact sheet. The prompt asks for a JSON object keyed by those labels. The script rejects answers with duplicate, missing or unexpected IDs.

## Lesson

Do not rely on the order of images in a request to identify them. Put the identifier in the pixels, and check that every requested ID comes back exactly once.

## Evidence

- The character audit, "What the full-book screen measured".
- The technical workflow record, sections 3 and 4, on labeled crop boards and response checks.
