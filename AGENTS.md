# AGENTS.md: start here

**This is the single entry point for AI agents working in this repository.** Read it before running anything. Human readers can start with [README.md](README.md).

## What you are doing

You are helping digitize a printed Korean family genealogy (jokbo): from a cleaned scan to a reviewed layout, a rendered PDF and, optionally, a SQLite database. The scan is the evidence. Your readings and the models' readings are proposals until checked against it.

## Read in this order

1. [README.md](README.md): the workflow and the quickstart.
2. [CONCEPTS.md](CONCEPTS.md): the terms (person appearance, person candidate, restricted appearance and others).
3. The book configuration you were given, or [book configuration](docs/methods/book-config.md) if you must write one.
4. The [methods guide](docs/methods/) for the stage you are on.
5. The [journal lessons](journal/README.md) for that stage. Most mistakes in them are cheap to prevent and expensive to find later.

## Before you start

- Run the practice-book quickstart in the README and confirm the expected output. If it does not match, stop and report the difference before working on a real book.
- Set `JOKBO_BOOK_CONFIG` to the absolute path of the book's configuration, or pass `--book-config` to each script. Confirm which book you are working on.
- Ask for a spending limit before any paid model call. A job limit in a script (`--max-jobs`) counts jobs, not money, and each job can retry.
- Do not overwrite inputs. Every script here writes new outputs and refuses to replace existing ones; keep it that way.

## Stages

| Stage | Guide | Main tools |
|---|---|---|
| Find the book and related records | [finding a clan branch jokbo](docs/methods/finding-a-clan-branch-jokbo.md), [finding archive household records](docs/methods/finding-archive-household-records.md) | none |
| Clean scan, page map, openings | [transcription and glyph review](docs/methods/transcription-and-glyph-review.md), section 1 | none shipped |
| Geometry and crops | same guide, section 3 | `map_layout.py`, `prepare_review.py` |
| Vision-model readings | same guide, section 4 | `read_regions.py`, `parallel_review.py` |
| Glyph and editorial review | same guide, section 5; [editorial review](docs/methods/editorial-review.md) | `review_ledger.py`, `compare_characters.py`, `apply_corrections.py` |
| Layout | [layout format](docs/methods/layout-format.md) | a text editor and the scan |
| Rendering | [rendering and fonts](docs/methods/rendering-and-fonts.md) | `build.py`, `build_book.py` |
| Proofing | [whole-book proofing](docs/methods/whole-book-proofing.md) | `audit_proof.py`, `review_report.py` |
| Database import | [database import](docs/methods/database-import.md) | `database/ingest.py` and the candidate scripts |

The tools in the middle column are in `pilot/convert-to-digital/` unless a path is given.

## Keep a run record for every stage

As the work happens, keep a durable technical record linked to its source files. Record:

- the objective;
- start and end times in a stated time zone, when measured;
- exact inputs and their SHA-256;
- commands and settings;
- outputs and their SHA-256;
- counts and verification results;
- decisions, errors, limitations and remaining work.

For each AI-assisted step, also record:

- the provider (for example OpenRouter) and the exact model requested and served, with version where available;
- reasoning or thinking settings;
- the prompt, or a reference to the prompt file;
- usage and cost when the provider reports them;
- whether a human or a model made the decision.

When a detail was not recorded, say so. Never reconstruct an exact setting, runtime or cost from memory or file timestamps.

## Capture durable learnings (optional)

At the end of each completed stage, ask whether anything non-obvious was learned that the code, tests and run record do not already show: a failure mode, a reason a method was chosen, a check that caught something. If so, write it up as a short, dated, source-linked note. Tools such as a compound-engineering style "learning capture" step can help, but any format works. If nothing qualifies, write "no learning recorded" and why in the run record. Do not invent one. A learning supplements the run record; it does not replace it.

Do not report a stage or review as complete if its record has not been written.

## Reviewing the original

**Before choosing between competing transcriptions, compare the printed occurrences in the scan.** Check the crop position, the distinguishing strokes and the character's role in its line. Once the scan shows that several occurrences are the same character, bind those locations to one Unicode reading. That reading governs transcription, rendering and database import.

**Record every differing OCR or model answer as a conflict with the verified reading.** This includes disagreements between two runs of the same model and cases where several models agree on a different answer. Keep the raw readings and their locations.

- If a crop is misplaced, blurred or too short to line up with the reading, leave that occurrence open.
- Reopen a verified reading only on new evidence from the source, and record why.
- A circle can be a number, a separator or a name placeholder. Encode it by its role, following the book's approved convention.
- Model agreement is evidence, not confirmation. Two models can read the same wrong row when the crop is misplaced.
- Model explanations can be invented. Check the scan, not the reasoning.

The full procedure, with worked examples, is in [editorial review](docs/methods/editorial-review.md).

## Edition-specific defaults

Some readings are settled by a written convention for one edition, not by the glyph. Apply such a default only within the edition that adopted it.

**Worked example.** In the 1989 Anseong Lee jokbo, the Hanja 진 is printed in a form that maps to either `鎭` or `鎮`. That edition's rule is: transcribe `鎭` throughout unless a specific impression in the original clearly shows `鎮`. Use `鎭` for an indistinct instance and label its basis as an editorial default. A clear contrary printing warrants a location-specific exception. Model output alone cannot establish one. The rule applies to this pair in this book only.

For your book, put defaults like this in:

- the `[editorial]` table of the book's configuration file, and
- the edition's editorial notes, labelled as conventions.

Do not carry a default from one book to another without checking the second book's print.

## When to stop and ask

Stop and ask the person you are working for when:

- a paid run would exceed the agreed limit, or no limit was agreed;
- an input's fingerprint does not match its manifest or page map;
- you would have to change an input file, a verified reading or a recorded decision without new source evidence;
- a reading affects a name, date or family link and the scan does not settle it (leave it open and report it instead of guessing);
- you are about to publish anything that names living people or people whose birth year is unknown. Read the README's privacy model first.

## What not to do

- Do not treat text extracted from a rendered PDF as the transcription. Use the layout.
- Do not merge two person appearances because their names match.
- Do not convert calendars or normalize variant characters in the transcription. Keep the print; put interpretations in separate fields.
- Do not delete raw model responses, even wrong ones.
