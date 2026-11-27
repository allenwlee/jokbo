# Rendering and fonts

Rendering turns a reviewed [layout](layout-format.md) into a PDF: one landscape page per opening, black text set in a real font, vector rules and frames, photographs cropped from the scan, and selectable, searchable text. The renderer is `pilot/convert-to-digital/build.py`. It reads the layout and does no OCR and no genealogy inference.

```sh
python pilot/convert-to-digital/build.py examples/synthetic-book/layout.json \
  --source examples/synthetic-book/scan/spreads.pdf \
  --font fonts/UnGungseo.ttf --fallback fonts/SourceHanSerifKR-VF.ttf \
  --output work/synthetic-digital.pdf
# 3 spread(s), 37 text runs, 61,272 bytes   (the size varies slightly between runs)
```

`--source` is the cleaned spreads PDF; the renderer measures ink on it and crops photographs from it.

## Font fallback order

A Korean genealogy mixes common Hanja, rare Hanja, Hangul and symbols. No single font covered every character in the Lee book. The renderer takes one primary TrueType font (`--font`) and any number of fallbacks (`--fallback`, repeatable). For each character it uses the first font, in that order, whose character map contains it.

The order used for the Lee edition:

1. **UnGungseo**: names, descriptions, Hangul readings and generation labels. [Download](https://mirrors.ctan.org/fonts/unfonts-core/UnGungseo.ttf).
2. **Source Han Serif KR** (variable font): first fallback, for characters such as `妍` and `〇`. [Download](https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/Variable/TTF/Subset/SourceHanSerifKR-VF.ttf). Weight 400 for body text and 600 for titles and readings.
3. **Arial Unicode MS**: second fallback for the few characters neither font has. It is not freely downloadable; it is present on some macOS systems.

Page numbers use Times Roman.

If no font covers a character, the build stops and lists it. With only UnGungseo, the practice book fails:

```sh
python pilot/convert-to-digital/build.py examples/synthetic-book/layout.json \
  --source examples/synthetic-book/scan/spreads.pdf --font fonts/UnGungseo.ttf --output work/x.pdf
# build.py: error: missing font glyphs: 〇
```

Things that went wrong or needed care:

- **The order is a decision; write it down and check it.** One final build of the Lee book put Arial Unicode before Source Han Serif KR by mistake. The next reconciled build restored the intended order. `build.py` takes the fonts only from its command line, so write the intended order in the book configuration (`[fonts]`, see [book configuration](book-config.md)), pass the files in that order, and record the order in the render receipt.
- **A fallback does not validate a reading.** Switching fonts keeps the same Unicode value. If the transcription is wrong, the fallback font renders the wrong character faithfully.
- **Count fallback use per location.** Six early Lee openings had 142 visible fallback occurrences: 131 from Source Han Serif KR and 11 from Arial Unicode MS. A later 60-opening proof had 304. These are font substitutions, not unknown characters. Keep them separate from OCR recoveries and open readings.
- **Check font licences before distributing.** A PDF embeds parts of each font. Read each font's licence for embedding and redistribution terms before you share the PDF.

The renderer uses [PyMuPDF](https://pymupdf.io/licensing), which is available under AGPL-3.0 or a commercial licence. The code in this repository is MIT-licensed, but anything you distribute that bundles PyMuPDF is subject to PyMuPDF's terms.

## Optical adjustments

- `〇` and `○` render at 78% of the fitted size around their measured centres, with the spacing of the surrounding text. The value is a constant in `build.py`; the book configuration records the same value as `circle_glyph_scale`.
- Full-width parentheses in vertical runs are rotated to follow the reading direction and set at 80%. Their characters are unchanged.
- The renderer fits each glyph by measuring scan ink in a window around its position. A window that reaches a neighbouring column picks up the wrong ink and misplaces the glyph. In the Lee afterword, narrowing the window and correcting measured centres fixed crowded pairs; see the [journal lesson on the measuring window](../../journal/lessons/2026-11-27-131412-renderer-measuring-window.md).

## Unicode round-trip

After saving, the renderer reopens the PDF and checks, for every opening, that the page label matches, that the number of embedded images equals the number of `photos`, and that the visible text equals the folios plus every run's text in layout order. Any difference stops the build and no output file is written. `database/test_synthetic_book.py` runs the same check on the practice book and also confirms that both circle forms, the placeholder `□` and the reference `一一一` come back out of the PDF.

The PDF also carries an invisible search copy of multi-character columns, because some viewers cannot find a complete vertical string in the visible text alone. The cost is that some viewers and extractors return text twice. In one Lee test, removing the search copy fixed duplicated extraction but made PyMuPDF find none of 4,642 tested complete columns; with it, all 4,642 were found. The edition kept the search copy. Use the layout, not PDF extraction, as the text source.

## Subset every font you embed

**Subsetting** means embedding only the glyphs a document uses instead of the whole font file. The renderer subsets its fonts. The Lee assembly step that adds editorial notes (`pilot/convert-to-digital/build_book.py`) at first embedded the whole Arial Unicode font for a few pages of notes. Subsetting that font to the characters actually used in the notes, opening labels, identifiers and punctuation reduced the assembled draft from 23,621,527 bytes (23.6 MB) to 8,442,673 bytes (8.4 MB).

How that change was checked, and how to check yours:

- extracted text and page labels identical on every page before and after;
- equal annotation counts;
- rendered samples of several openings and the notes page compared pixel by pixel (they were identical);
- the coverage check still runs against the complete font before subsetting, so a missing glyph is still caught.

Collect the characters from every part of the PDF (body, notes, labels, punctuation) before you subset, or a late addition renders as a missing glyph.

## Receipts

Record the SHA-256 of the layout, the source PDF, every font file and the output, plus the font order, for each build. A receipt shows which files made a PDF. It does not show that the transcription is right; only review does that.
