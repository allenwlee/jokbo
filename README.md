# jokbo: digitizing a printed Korean family genealogy

This repository shows how to turn a printed Korean family genealogy (a **jokbo**, 족보) into a digital edition: a PDF that looks like the original pages but has real, searchable text, and optionally a database in which every name, date and family link points back to the exact place it is printed.

It is for families, researchers and AI agents who have a jokbo, or are about to scan one, and want a careful copy that relatives can search and read without handling a fragile book. It records the methods that worked on one full book, the code that carried them out, a small made-up practice book to try them on, and a journal of every mistake made along the way.

The book behind it is the 1989 genealogy of the Jangsu branch of the Anseong Lee clan: 137 numbered pages, mostly in Hanja (Chinese characters as used in Korean writing) with some Hangul (the Korean alphabet), much of it in family charts read top to bottom and right to left. None of that book's scans or data are in this repository. Everything you can run here uses the practice book, whose names are all fictional.

## Why do it this way

Off-the-shelf OCR (optical character recognition, software that reads text from images) and AI vision models misread genealogies in ways that are hard to spot: a model's suggested correction turns 1965 into 1945, a dropped stroke shortens a page reference, a crop placed one row off gives two models the same wrong name, a rare character is silently swapped for a common one. The approach here keeps three things apart at every step:

- **the scan**, which is the evidence;
- **the reviewed transcription**, which records what an editor decided the scan says, and where;
- **everything proposed by software or models**, which stays a proposal until someone checks it against the scan.

## The normal workflow

1. **Clean the scan.** Remove duplicate captures, put the pages in book order, and pair facing pages into **openings** (two facing pages scanned together). Write a **page map**: one record per page side with its printed page number, if any, its position in book order, and the transform from the raw scan to the cleaned page. Freeze both files and record their SHA-256 fingerprints.
2. **Propose layout geometry.** Detect text regions and ruled lines on each cleaned page. These boxes are a starting point and are often wrong.
3. **Transcribe with vision models.** Cut each text run out as a labelled crop and have two or more vision models read it without seeing the draft text. Record every answer, the model and its cost.
4. **Review glyphs against the scan.** Where readers disagree, or where a name or date matters, compare the printed character with clear printings of it elsewhere in the book, then decide. Record every model answer that differs from the decision as a conflict. Leave unclear characters open.
5. **Write the layout.** The reviewed layout is a JSON file listing every run of text with its position, plus rules, frames, page numbers and photographs.
6. **Render a PDF.** The renderer draws each opening from the layout in real fonts, checks that the text in the PDF matches the layout exactly, and adds a search copy. An assembly step adds editorial notes. This gives the original-language edition; a translated or bilingual edition is built on top of it, and that step is not part of this repository's code.
7. **Import to SQLite (optional).** Load the layout into a database as **person appearances** (each mention of a possible person in one place), with facts and links that each carry a review status.
8. **Proof the whole book.** Compare every rendered opening with its scan in book order, fix what is wrong in a new layout revision, and render again.

The [methods guides](docs/methods/) explain each step in detail.

## Quickstart on the practice book

The practice book in `examples/synthetic-book/` has three openings (six page sides) with a generation chart that continues across a page, an ink blot transcribed as `□`, both circle characters `〇` and `○`, an index reference `一一一`, Hanja names printed with Hangul readings, and one text run deliberately placed in the wrong spot.

You need Python 3.11 or later. Run everything from the repository root.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r pilot/convert-to-digital/requirements.txt
export JOKBO_BOOK_CONFIG="$PWD/book-config/synthetic.toml"
mkdir -p work fonts
```

`JOKBO_BOOK_CONFIG` tells every script which book it is working on. Use an absolute path, as here.

### 1. Get two fonts

The renderer needs TrueType fonts that cover Hanja and Hangul. These two are free to download:

```sh
curl -L -o fonts/UnGungseo.ttf https://mirrors.ctan.org/fonts/unfonts-core/UnGungseo.ttf
curl -L -o fonts/SourceHanSerifKR-VF.ttf \
  https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/Variable/TTF/Subset/SourceHanSerifKR-VF.ttf
```

### 2. Run the practice-book tests

```sh
python -B -m unittest discover -s database -p 'test_synthetic_book.py' -v
```

Expected: `Ran 9 tests` and `OK`. The tests import the practice book into a database, propose names and chart entries, find the cross-page continuation, flag the misplaced crop, and render a PDF and check its text. The rendering test uses the fonts listed under `[fonts] files` in `book-config/synthetic.toml`, which are macOS system fonts. On another system it is skipped; put the paths of the two downloaded fonts in that list to run it.

### 3. Make review crops

```sh
python pilot/convert-to-digital/prepare_review.py examples/synthetic-book/layout.json \
  --source examples/synthetic-book/scan/spreads.pdf \
  --page-map examples/synthetic-book/scan/page-map.json --output work/review
```

Expected: `3 openings, 37 regions, 8 source crop boards, 1 crops with almost no scan ink`. Open `work/review/*.png` to see the labelled crops. The one nearly blank crop is the misplaced run; `work/review/manifest.json` lists it under `low_ink_crops` as `S001-L-0013-000`. Sending crops to vision models (`read_regions.py`) needs an OpenRouter API key and costs money, so the quickstart stops before that step.

### 4. Render the PDF

```sh
python pilot/convert-to-digital/build.py examples/synthetic-book/layout.json \
  --source examples/synthetic-book/scan/spreads.pdf \
  --font fonts/UnGungseo.ttf --fallback fonts/SourceHanSerifKR-VF.ttf \
  --output work/synthetic-digital.pdf
```

Expected: `3 spread(s), 37 text runs, ` followed by the file size (about 61 KB with these fonts). Open the PDF and search for `明德`. Try it once without `--fallback`: the build stops with `missing font glyphs: 〇`, because UnGungseo has no `〇`. That is the reason for the fallback font.

### 5. Compare the proof with the scan (optional)

This step needs OpenCV:

```sh
python -m pip install opencv-python
python pilot/convert-to-digital/audit_proof.py \
  --source examples/synthetic-book/scan/spreads.pdf --proof work/synthetic-digital.pdf \
  --layout examples/synthetic-book/layout.json --output work/proof-audit
```

Expected: `Spatially compared 3 printed openings`. In `work/proof-audit/spatial-review.local.json`, the left page of opening 1 shows unmatched ink in two places: where the layout put the misplaced run, and where the scan really prints it.

### 6. Build the database

```sh
python database/ingest.py work/book.sqlite
python database/candidate_people.py work/book.sqlite work/candidates.sqlite work/candidates.json
python database/candidate_embedded.py work/candidates.sqlite work/embedded.sqlite work/embedded.json
python database/chart_rules.py work/candidates.sqlite work/chart-rows.json
python database/group_entries.py work/candidates.sqlite work/entries.sqlite work/entries.json \
  --measurements work/chart-rows.json
sqlite3 work/entries.sqlite "select relation_type, count(*) from passage_links group by 1;"
```

Each step prints a JSON receipt. Expected counts: 11 name candidates, 2 embedded names (a spouse designation after the spouse marker 配, and `正植` after the father marker 父), 12 proposed entries, and the query prints `contains|11` and `possible_continuation|1`. The scripts never overwrite an existing file, so delete `work/` before running them again.

### 7. Regenerate the practice book (optional)

```sh
python examples/make_synthetic_book.py --output work/synthetic-book --font fonts/UnGungseo.ttf
```

Expected: `3 openings, 6 pages, 37 runs written to work/synthetic-book (font: UnGungseo.ttf)`. The shipped files were drawn with AppleMyungjo, so a book drawn with another font has different fingerprints. Without `--output` the script overwrites `examples/synthetic-book/`.

## Using it on your own book

1. Copy `book-config/synthetic.toml` and describe your book in it: paths, counts, page size, chart markers, fonts and editorial defaults. See [book configuration](docs/methods/book-config.md).
2. Produce a cleaned spreads PDF and a page map in the format of `examples/synthetic-book/scan/page-map.json`.
3. Follow the [methods guides](docs/methods/) in order. Start with one dense opening and check it fully before doing the rest.

If an AI agent is doing the work, point it at [AGENTS.md](AGENTS.md) first.

## How the repository is organised

| Path | What it holds |
|---|---|
| `AGENTS.md` | The entry point for AI agents: workflow, record-keeping rules and review rules. |
| `docs/methods/` | One guide per stage, from layout format to proofing and database import. |
| `docs/solutions/workflow-issues/` | Research guides: finding a branch's jokbo in library catalogues, and finding archive household records. |
| `book-config/synthetic.toml` | The practice book's configuration, and the template for yours. |
| `examples/` | `make_synthetic_book.py` and the practice book it generates. |
| `pilot/convert-to-digital/` | Crop review, model reading, review ledger, corrections, rendering and proof comparison, with their tests. `examples/synthetic-layout.json` is the smallest layout example. |
| `pilot/schema.sql`, `database/` | The SQLite schema and the import and candidate scripts, with `book_config.py`, which loads the book configuration. |
| `publish/` | The tools used to publish this repository safely (see below). |
| `research/hojok-samples/` | Five public-archive household records with their source links and transcriptions. |
| `journal/` | What happened at each stage, what it cost, and every documented mistake. |
| `history-video/` | How a short narrated map video about the book's history was made. |
| `CONCEPTS.md` | A glossary of the terms used across the project. |

The pieces connect through files, not a server. The cleaned scan and page map feed the review tools; the review produces a layout; the layout feeds both the renderer and the database import. Each tool checks the fingerprints of the files it is given, writes new outputs rather than editing old ones, and prints a receipt.

## Privacy model

A genealogy is about real people, many of them alive. This repository was published from a private working repository under rules set by the maintainer. The method can be reused for any similar project.

**The rule.** People whose recorded birth year is 1920 or earlier may appear in full: names, dates, relationships, page images. Everyone else appears only as a short glyph or reading needed to explain a lesson, with no page number, date or relative attached. Anyone whose birth year is missing, or whose year cannot be verified, counts as born after 1920. Totals and statistics may count everyone, as long as no figure points to one person. The maintainer is anonymous. The book itself may be named.

**How it is applied.**

1. **A privacy register.** `publish/privacy_register.py` classes every person appearance in the edition database as `open` or `restricted`, by appearance ID and location, never by name, because the same name belongs to people on both sides of 1920. An own birth claim opens an appearance only if it holds a complete four-digit year of 1500 or later, any cycle-year label agrees with that year, and every other birth claim for that appearance is also 1920 or earlier. Relatives' dates can only restrict, never open. Three-digit years that a model shortened (a 1958 stored as "0958") stay restricted.
2. **An allowlist export.** `publish/export.py` copies only files that are listed by name in an allowlist manifest into a separate folder outside the working repository. Anything not listed stays private, including every new file. Prose about the book, such as these guides and the journal, is rewritten by hand for publication rather than redacted automatically, and every mention of a person from the book is tied to its appearance ID in a private sidecar file.
3. **A leak gate.** `publish/check.py` scans the exported folder before anything is committed. It looks for restricted names in Hanja, Hangul and romanized forms, years after 1920 near names, relationship markers next to restricted names, identity strings, secrets, and image and PDF metadata; it checks that every image and PDF is individually approved and classed. Any finding stops the release.
4. **Fresh history.** The public repository is a new repository that receives only exports that passed the gate. The working repository's history, which holds the scans and data, is never pushed to it.

The register and the gate need the edition database and a private list of identity terms, neither of which is published. To reuse them, build your own edition database and run them against it.

## Licences

- Code is under the MIT licence: see [LICENSE](LICENSE).
- Prose, including the journal, these guides and the method documents, is under Creative Commons Attribution 4.0 International (CC BY 4.0): see [LICENSE-docs](LICENSE-docs).
- The archive images in `research/hojok-samples/` come from public archives and are not covered by either licence; each has its source link beside it.
- The renderer depends on [PyMuPDF](https://pymupdf.io/licensing), available under AGPL-3.0 or a commercial licence. Fonts carry their own licences. Check both before you distribute a PDF or a bundled tool.

## The journal

The [journal](journal/README.md) records every stage of the original project in date order, the models, providers and costs, and each documented mistake: what happened, how it was noticed, what it affected, what fixed it, and the lesson. If you are about to start on your own book, read the lessons first.
