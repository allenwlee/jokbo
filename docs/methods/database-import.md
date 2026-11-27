# Database import

This step is optional. It loads the reviewed layout into a SQLite database so the book can be searched and queried: who appears where, which facts each entry states, and which links between people have been proposed or checked. Every record points back to the exact printed text it came from.

## Appearances, not people

The database is built around **person appearances**. An appearance is one mention of a possible person in one place in the book: a chart cell, a name inside a relative's entry, an index line. The same historical person usually appears several times, for example once in a chart cell, once in the index and once as a parent named in a child's entry. Those are separate appearances until someone shows, from the source, that they are the same person.

This matters because:

- names repeat across generations and branches, so matching by name merges different people;
- a fact belongs to the passage that states it, and two passages can disagree;
- a merge made too early is hard to undo, while two separate appearances can always be linked later.

A **person candidate** is an appearance that a script or model proposed and nobody has reviewed. Treat every candidate as unconfirmed.

## Schema

`pilot/schema.sql` is the base. `database/schema-extension.sql` is applied on top of it in a new database: it renames three tables and adds five.

| Table | What it holds |
|---|---|
| `source_assets` | The exact bytes of the scan, cleaned spreads, layout and page map, with file type and SHA-256. |
| `spreads` | One row per opening, with its scan and layout asset and canvas size. |
| `layout_runs` | Every positioned text run, addressed by opening and run index, with text, position, style, pitch and size. A run is not a person. |
| `source_passages` | Pages, regions, entries and other passages, with printed page number, book-order sequence, scan side, bounding box and coordinate space, review status. |
| `passage_runs` | Which runs (and which character offsets in them) make up a passage. An entry can span several runs or openings. A trigger rejects offsets past the end of the run. |
| `passage_links` | Links between passages, such as a heading and the entries it covers, or a possible continuation of an entry onto the next page. Each has a review status. |
| `people` | One row per appearance ID. |
| `names`, `name_forms` | Names attached to an appearance, each form with its script, kind and source passage. |
| `facts` | Claims about an appearance: birth, death, burial, residence, courtesy name and so on, with the original text, the date as written, cycle year, calendar and review status. |
| `relationships` | Proposed or checked links between appearances, with their basis, original label, review status and optional rule ID, rule version and evidence reference. |
| `places` | Place records, with coordinates only when a source passage supports them. |
| `assets` | Images associated with an appearance, with the subject's box and an identity confidence. |

`database/dossier_views.sql` adds two views: `dossier_entries` (each appearance with its entry text and page) and `birth_year_claims` (each dated birth fact with its review status and source passage).

Coordinates always say which space they are in. Layout runs use the cleaned opening with its top-left origin. Raw-scan page records say `original_scan_pixels` and keep the page-map transform. Never mix the two.

In a `relationships` row of type `parent`, the first person is the child and the related person is the parent.

## Review status is part of every claim

A fact, name, passage, link or relationship carries its own `review_status`. Values used in this project:

| Status | Meaning |
|---|---|
| `unreviewed_candidate` | Created by a deterministic script; not looked at. |
| `geometric_proposal` | Grouped by position on the page (rows, columns, rules); not looked at. |
| `model_proposal` | Proposed by a vision or language model reading the page; not looked at. |
| `focused_review_proposal`, `gap_review_proposal`, `sparse_review_proposal` | Proposed by a later, narrower model pass over specific entries or gaps; still proposals. |
| `proposed` | Proposed by hand; not yet checked. |
| `layout_checked` | Checked against the printed layout by a person. |
| `family_supplied` | Supplied by a family member, not printed in the book. Keep it distinct from the print. |

Name forms also have a `form_kind`: `printed`, `person_supplied`, `family_supplied`, `documented`, `editorial_reading` or `generated_romanization`.

In the Lee edition, 3,793 of 4,732 fact records and 1,576 of 1,580 relationship records were still `model_proposal`. Some facts repeat one statement from two sources, so counting birth rows double-counts some appearances. When a printed date and a family-supplied date disagree, keep both; a query for one person's birth year must not count them as two people.

## Run it on the practice book

From the repository root, with `JOKBO_BOOK_CONFIG` set as in the quickstart:

```sh
python database/ingest.py work/book.sqlite
python database/candidate_people.py work/book.sqlite work/candidates.sqlite work/candidates.json
python database/candidate_embedded.py work/candidates.sqlite work/embedded.sqlite work/embedded.json
python database/chart_rules.py work/candidates.sqlite work/chart-rows.json
python database/group_entries.py work/candidates.sqlite work/entries.sqlite work/entries.json \
  --measurements work/chart-rows.json
```

What each step does:

1. `ingest.py` checks the layout and scan fingerprints against `examples/synthetic-book/manifest.json` and the page map, then writes a new database with 3 spreads, 6 page records and 37 layout runs. It refuses to overwrite an existing file, and removes a partial output on failure.
2. `candidate_people.py` proposes name candidates from large chart-name runs: 11 on the practice book, 10 introduced by an entry marker (子 or 女) and 1 found by a Hanja name sitting next to a Hangul reading. It creates no facts or relationships.
3. `candidate_embedded.py` adds names found after a spouse marker (配) or a father marker (父): one spouse designation and `正植` on the practice book. A spouse designation keeps its clan and place wording as printed; it is not a modern full name.
4. `chart_rules.py` measures the horizontal rules between generation rows on the scan, for the chart pages set in the configuration.
5. `group_entries.py` groups runs into proposed entries using those rows: 12 on the practice book, plus one `possible_continuation` link for an entry that continues from printed page 2 to page 3.

Each command prints a JSON receipt with start and end times (JST), input and output SHA-256, counts, the models used (none for these steps) and known limits. Keep the receipts. Every output must be a new file; the scripts refuse to replace one.

Look at the result:

```sh
sqlite3 work/entries.sqlite "select relation_type, count(*) from passage_links group by 1;"
# contains|11
# possible_continuation|1
```

## On a real book

- Import only the reviewed layout. The PDF's extracted text can duplicate or reorder vertical text.
- Do not substitute a different layout revision: positions and review decisions are tied to one revision's hash.
- Model-assisted stages that read page images and propose facts and relationships come after these steps. Record provider, model, prompt and cost for each, and import their output as `model_proposal`.
- Relationship inference needs the chart geometry and source-backed review. On one Lee calibration page, 2 of 10 proposed parent choices were wrong.
- Dates are recorded as written. `database/claim_dates.py` reads year, month and day precision from a literal Hanja date; it does not convert calendars. A model can drop a leading digit or stroke from a year, so a three-digit year is a reading problem, not a date in antiquity.
