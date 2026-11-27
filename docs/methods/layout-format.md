# The layout file

A layout is a JSON file that says what text is printed on each opening of the book and exactly where. It is the reviewed transcription: the renderer draws the digital page from it, and the database import reads its text runs. The scan is the evidence; the layout is what an editor has decided the scan says.

An **opening** (also called a spread) is a pair of facing pages, photographed or scanned together. A **run** is one unbroken line of printed text, usually a vertical column.

The renderer is `pilot/convert-to-digital/build.py`. It checks every rule below and stops with an error that names the spread and field when the layout breaks one. Two examples ship with this repository:

- `pilot/convert-to-digital/examples/synthetic-layout.json`: one opening, six runs, the smallest useful file.
- `examples/synthetic-book/layout.json`: the three-opening practice book used by the quickstart.

## Top level

```json
{"spreads": [ { ...one opening... }, { ... } ]}
```

`spreads` is a non-empty array, in the order the openings should appear in the output PDF. One spread becomes one landscape PDF page.

## One spread

| Key | Required | Meaning |
|---|---|---|
| `source_page` | yes | One-based page number of this opening in the cleaned scan PDF passed with `--source`. |
| `width_px`, `height_px` | yes | The measurement canvas, in pixels, for the whole opening. Positive integers. |
| `label` | no | PDF page label, for example `"2-3"` for printed pages 2 and 3. Defaults to the `source_page` number. The renderer checks that the label survives into the PDF. |
| `scale` | no | PDF points per layout pixel. Default `0.4`. A 1200 × 800 canvas at 0.4 gives a 480 × 320 point page. |
| `columns` | no | Text runs (below). |
| `lines` | no | Straight rules: `[x1, y1, x2, y2, stroke_width_pt]`. |
| `rectangles` | no | Frames: `[left, top, right, bottom, stroke_width_pt]`. Width and height must be positive. |
| `circles` | no | Drawn circle marks: `[center_x, center_y, radius_px, stroke_width_pt]`. |
| `folios` | no | Printed page numbers: `[x, baseline_y, text, size_pt]`. Set in Times Roman, so the text must be printable ASCII. |
| `photos` | no | `[left, top, right, bottom]`. The renderer crops this box from the scan and places it at the same spot. |

All coordinates are layout pixels with `(0, 0)` at the top left of the **whole opening**, not of one page. Stroke widths and folio sizes are in PDF points. Every point must lie inside the canvas.

## Text runs

Each entry in `columns` is an array of three to seven values:

```
[x, y, text, style?, pitch?, size?, glyph_centers?]
```

- `x`, `y`: the centre of the first character.
- `text`: the printed characters in reading order. No spaces or invisible characters. An unreadable printed character is kept as a placeholder such as `□` rather than guessed.
- `style`: one of

  | Style | Default size px | Default pitch px | Use |
  |---|---:|---:|---|
  | `body` (default) | 26 | 27.5 | Ordinary vertical text |
  | `title` | 51 | 61 | Large chart names and headings |
  | `reading` | 24 | 26 | Hangul reading printed beside a Hanja name |
  | `generation` | 25 | 28 | Generation labels such as 第一世 |
  | `horizontal` | 26 | 27.5 | Left-to-right lines |
  | `horizontal_rtl` | 26 | 27.5 | Lines printed right to left, such as old photo captions |

- `pitch`: distance from one character centre to the next. Pass `null` to keep the default while still giving a size.
- `size`: character size in pixels.
- `glyph_centers`: one `[x, y]` pair per character, measured on the scan. The first pair must equal `[x, y]`, and the pairs must move in reading order (down for vertical runs, right for `horizontal`, left for `horizontal_rtl`). Use this when the printed spacing is uneven.

For a right-to-left book, list the right-hand page's runs first, then the left page's, each in reading order. The database import numbers runs by their position in this list, so keep the order stable once a layout has been reviewed.

## What the renderer does with it

- It measures ink on the scan around each run to refine position and size, so a run placed over the wrong text picks up the wrong ink. See [whole-book proofing](whole-book-proofing.md).
- `〇` and `○` render at 78% of the fitted size, centred, with the surrounding spacing. Full-width parentheses `（` `）` in vertical runs are rotated and set at 80%. Their Unicode values do not change.
- It writes visible text plus an invisible search copy, then re-reads the PDF and checks that every spread's label, image count and text match the layout exactly. A mismatch stops the build and no output is written.

## Example

The opening in `examples/synthetic-layout.json`, trimmed:

```json
{
  "source_page": 1, "label": "2-3", "width_px": 1200, "height_px": 800, "scale": 0.4,
  "folios": [[1120, 48, "2", 12], [63, 48, "3", 12]],
  "rectangles": [[624, 64, 1176, 754, 1.5], [24, 64, 576, 754, 1.5]],
  "lines": [[624, 380, 1176, 380, 0.65], [24, 380, 576, 380, 0.65]],
  "columns": [
    [1120, 115, "第一世", "generation"],
    [1000, 123, "子明德", "title"],
    [1000, 320, "명덕", "reading"],
    [945, 135, "一九四〇年生"]
  ]
}
```

The names are fictional.

## Checks before you trust a layout

- Copy the names, printed page numbers and chart lines back against the scan for one dense opening before laying out the rest.
- Keep each layout revision as a separate file and record its SHA-256. Review findings and corrections in this project are tied to a layout hash, so a moved or edited run gets a new finding instead of silently inheriting an old decision.
- Do not treat text extracted from the rendered PDF as the transcription. PDF viewers can duplicate or reorder vertical text. The layout is the source for search, translation and database import.
