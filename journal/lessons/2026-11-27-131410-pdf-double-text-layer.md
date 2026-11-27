# A PDF with two text layers returns characters twice

Appendix item: 17. Date: 21 November 2026 (JST).

Terms used here:

- The rendered proof PDF has **visible text**, drawn glyph by glyph in vertical columns, and an **invisible search index**, a hidden copy of each column that makes search work.
- **Text extraction** is pulling all characters out of a PDF with a library or viewer.

## Summary

On one opening, whole-page extraction with PyMuPDF 1.27.2.3 returned the character 户 twice where the visible column has it once. Apple's PDFKit on macOS 27.2.1 also returned two.

Removing the hidden index in a test copy fixed the duplicate. But then PyMuPDF found none of 4,642 tested column strings of four or more characters. With the index it found all 4,642. An experiment with the PDF `/ActualText` feature did not restore search.

## Impact

Anyone who extracted text from the PDF to build a database would have counted some characters twice. Fixing that by removing the index broke search.

## How it was noticed

A copy-and-search check compared extracted text with the visible column on a sample opening.

## Root cause

Both layers are real text in the PDF. Extraction tools read both and do not know that one exists only for search.

## Fix

The proof keeps its search index. The reviewed structured layout, with its page mapping, is the working transcription for the database. The PDF is not treated as a text source.

## Lesson

Do not use PDF extraction as the source of truth for a typeset genealogy. Keep the structured layout as the authority and treat the PDF as one output.

Test copy and search in more than one reader. The results here do not establish how every viewer behaves.

## Evidence

- The conversion work log entry "PDF copy/search check, 21 November".
- The technical workflow record, section 6.
