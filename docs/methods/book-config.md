# Book configuration

Everything that is specific to one book lives in a TOML file under `book-config/`, not in the code: file paths, page and opening counts, page size, chart vocabulary, font order, editorial defaults and the lines that describe the book inside model prompts. To work on a new book, copy `book-config/synthetic.toml`, edit it, and select your copy.

## Selecting a configuration

`database/book_config.py` picks the file in this order:

1. a path passed to a script with `--book-config FILE`;
2. the `JOKBO_BOOK_CONFIG` environment variable;
3. `book-config/lee.local.toml` if it exists (the original project's private configuration; it is not in this repository);
4. `book-config/synthetic.toml`, the practice book.

Give `JOKBO_BOOK_CONFIG` as an absolute path, for example `export JOKBO_BOOK_CONFIG="$PWD/book-config/synthetic.toml"`. A relative value is resolved from whatever directory a command runs in, so tests started from another folder will not find it. Relative paths *inside* the file resolve against the repository root (the parent of `book-config/`).

Loading fails with an error naming the key when a required key is missing, when `counts.openings`, `counts.pages`, `canvas.page_width_px` or `canvas.page_height_px` is not a positive integer, or when `chart.cycle` does not list 60 names.

## Keys

Required keys are marked **R**. "Read by" lists the shipped scripts that use the key today. A required key with no reader is still validated, and records a decision that review must apply by hand until a script reads it.

### `[book]`

| Key | | Meaning | Read by |
|---|---|---|---|
| `id` | R | Short identifier for this configuration. | tests |
| `edition_key` | R | Stored on every page record in the database; identifies which printed edition the scan comes from. | `ingest.py` |
| `pdf_title` | R | Title written into the assembled book PDF. | `build_book.py` |
| `pdf_subject` | | Subject written into the assembled book PDF. | `build_book.py` |

### `[prompts]`

Filled into `{{name}}` placeholders in the model prompt files `database/*prompt*.txt`. Any placeholder left unfilled is an error, so a prompt cannot go out describing the wrong book.

| Key | | Meaning |
|---|---|---|
| `book_identity` | R | How the page-extraction prompt names the book, as in "the {{book_identity}} genealogy". |
| `book_identity_audit` | R | How the second-reader audit prompts name the book, as in "this page of the {{book_identity_audit}} jokbo". |
| `book_description` | R | A short description for the people-indexing prompt, for example "typeset synthetic Korean family genealogy". |

### `[paths]`

| Key | | Meaning |
|---|---|---|
| `layout` | R | The reviewed layout JSON (see [layout format](layout-format.md)). |
| `manifest` | R | Fingerprints tying the layout to the cleaned scan. `ingest.py` refuses inputs whose SHA-256 does not match. |
| `scan` | R | The cleaned spreads PDF, one page per opening. |
| `original` | R | The raw scan, stored in the database as a source asset. Its SHA-256 must match the page map. |
| `page_map` | R | Page sides, printed page numbers, book order and raw-to-clean transforms. |
| `row_measurements` | R | Where `chart_rules.py` output is expected by `group_entries.py` and later steps. |
| `trial_output` | R | Output folder for the small instrumented model trial (`trial_people.py`). |

### `[counts]`

| Key | | Meaning |
|---|---|---|
| `openings` | R | Number of openings. `ingest.py` checks that the layout covers each opening exactly once. |
| `pages` | R | Number of page sides, including unnumbered and blank ones. `ingest.py` checks that the page map covers each exactly once. |
| `layout_runs` | | Expected number of text runs; `ingest.py` checks it when present. |

### `[canvas]`

| Key | | Meaning |
|---|---|---|
| `page_width_px` | R | Width of one cleaned page side in pixels. An opening is twice this. |
| `page_height_px` | R | Height of one cleaned page side in pixels. |

### `[chart]`

| Key | | Meaning | Read by |
|---|---|---|---|
| `first_page`, `last_page` | R | Printed page range holding generation charts. | candidate and grouping scripts |
| `entry_markers` | R | Characters that introduce a chart entry. In the practice book, 子 (son) and 女 (daughter). | `candidate_people.py` |
| `spouse_marker` | R | Introduces a spouse (配). | `candidate_embedded.py` |
| `father_marker` | R | Can introduce the spouse's father (父). | `candidate_embedded.py` |
| `cycle` | R | The 60 sexagenary-cycle year names, in order. Used to find where spouse and father phrases end. | `candidate_embedded.py` |
| `large_size` | R | A run is treated as a large name heading when its style is `title` or its size is at least this many pixels. | `candidate_people.py`, `group_entries.py` |
| `row_centers` | R | Expected y positions of the horizontal rules between generation rows, in page pixels. | `chart_rules.py` |
| `rule_scan_x` | R | Page-local x range sampled when measuring those rules on the scan. | `chart_rules.py` |
| `right_margin_exclude_x` | R | Runs on the right page beyond this opening x position are generation labels, not entries. | `group_entries.py` |

### `[candidates]`

| Key | | Meaning |
|---|---|---|
| `baseline_count` | | `candidate_embedded.py` refuses an input database that does not hold exactly this many name candidates, so it cannot run on the wrong stage's output. 11 for the practice book. |

### `[draft]`

Used by `pilot/convert-to-digital/assemble_draft.py` when it draws index and chart pages.

| Key | Meaning |
|---|---|
| `index_first_page`, `index_last_page` | Printed page range of index pages that use fixed rule guides. |
| `index_rule_guides` | Fixed rule positions for those index pages (empty in the practice book). |
| `chart_rule_first_page`, `chart_rule_last_page` | Printed page range whose rules come from chart measurements. |
| `index_reference_band_y` | `[top, bottom]` band holding page references, excluded from index-page rule detection. |

### `[fonts]`

| Key | | Meaning | Read by |
|---|---|---|---|
| `order` | R | Font names in fallback order, as a record of the decision. | none yet |
| `files` | | Font files in the same order. The first one that exists is primary. | `make_synthetic_book.py`, `test_synthetic_book.py` |
| `circle_glyph_scale` | R | Size of `〇` and `○` relative to the column size. `build.py` uses its own constant, 0.78; keep them equal. | none yet |

`build.py` takes fonts from its command line, not from this file. The practice configuration lists `AppleMyungjo` and `Arial Unicode MS`, which exist on macOS. On another system, put the paths of fonts you have in `files`, for example UnGungseo and Source Han Serif KR (see [rendering and fonts](rendering-and-fonts.md)). If none of the files exists, the renderer test is skipped, not failed.

### `[editorial]`

| Key | | Meaning | Read by |
|---|---|---|---|
| `jin_default` | R | The default encoding when two Unicode characters print identically in this edition. | none yet |
| `jin_variant` | | The other encoding, used only at locations where the scan clearly shows it. | none yet |
| `circle_forms` | R | Circle characters kept distinct: `〇` (U+3007) and `○` (U+25CB). | `make_synthetic_book.py`, tests |
| `title_page_sequences` | | Book-order sequences of title pages whose model readings are replaced by an editorial exclusion. | `finalize_book.py` |

The `jin_*` keys are named after the Lee book's 鎭/鎮 pair (see [editorial review](editorial-review.md#edition-specific-defaults)). Another book may need a different pair or none. When you add a default of your own, put it here and in the edition's editorial notes, and say in the notes that it is a convention.

## Adapting it to your book

1. Copy `book-config/synthetic.toml` to a new file and change `[book]` and `[prompts]` first, so nothing you produce is labelled as the practice book.
2. Point `[paths]` at your cleaned scan, page map, layout and manifest.
3. Fill `[counts]` and `[canvas]` from your page map.
4. Read a few chart pages and fill `[chart]`: markers, rule positions, label margin. Run `chart_rules.py` and check that each measured rule has basis `scan`, not a template fallback.
5. Decide the font order and any editorial defaults, and write them in `[fonts]` and `[editorial]`.
6. Select the file with `--book-config` or `JOKBO_BOOK_CONFIG` and run the database steps one at a time, reading each receipt.
