# Whole-book proofing

Proofing compares every rendered opening with its scan, in book order, before the edition is called finished. Character review checks what each glyph is. Proofing checks that everything is there and in the right place: no missing column, no text drawn over another, no broken frame, no chart line dropped, and that page order and cross-page links still hold after every correction.

## Freeze, then compare

1. Record the SHA-256 of the cleaned scan, the layout and the rendered PDF. A proof result applies only to that combination.
2. Go through every opening in the original order and keep a coverage record: which openings were compared, at what scale, by whom or by which tool, and what was found.
3. Show the scan and the proof at the same scale, side by side, with enlarged crops of the matching details.
4. Use an ink-difference screen to point at candidate problems, then look at each flagged area on the scan.
5. Check character readings separately, at readable magnification: names, dates, cross-page chart references and editorial notes. A page-scale comparison cannot tell a right glyph from a wrong one in the right place.
6. Turn each accepted correction into a new layout revision, render it again, and check the corrected area against the scan again.
7. State the exact scope in the report: what was inspected, what was only screened, and what is still uncertain.

## The ink-difference screen

`pilot/convert-to-digital/audit_proof.py` (needs OpenCV: `python -m pip install opencv-python`) rasterises each opening of the scan and of the proof, and reports ink in one that has no ink nearby in the other, within a tolerance in pixels (default 10). It writes a comparison image per opening and a JSON report with the unmatched fractions and the largest clusters per page side, plus a separate three-pixel page-edge screen.

```sh
python pilot/convert-to-digital/audit_proof.py \
  --source examples/synthetic-book/scan/spreads.pdf --proof work/synthetic-digital.pdf \
  --layout examples/synthetic-book/layout.json --output work/proof-audit
# Spatially compared 3 printed openings
```

On the practice book, the left page of the first opening shows unmatched proof ink where the layout puts the misplaced run, and unmatched scan ink 150 layout pixels away, where the scan actually prints it. That pair of clusters is the signature of a misplaced run.

How to read the numbers:

- **They screen placement, not correctness.** A glyph can sit in exactly the right place and be the wrong character.
- **Expect false alarms.** Font shapes differ from the printed type, scans are skewed, ink bleeds through from the other side of the paper, and photographs never match. Each flagged cluster needs a look at the scan.
- **The page-edge screen is noisy.** It flags text and scan noise near the edges as well as missing borders.

On 60 openings of the Lee book at 10-pixel tolerance, the mean unmatched scan ink was 0.169% and the mean unmatched proof ink 2.018% across 120 page sides. Those are screening indicators for that proof only.

## What full-book proofing caught in the Lee edition

- A date drawn over a name on one page, although the transcription of both was correct. The layout positions were wrong.
- An incomplete inner border on one page, later rebuilt as four continuous lines from the surrounding scan geometry.
- A missing `一` in a generation column, found by comparing only the right-edge strip of every page.
- Duplicate runs left behind when two layout revisions were combined. Removing them safely meant applying every correction by original opening, run and character offset first, then deleting duplicates from the highest index down so earlier indices did not shift.

Rechecking each corrected crop against the scan is what established the fixes, not the rebuild passing.

## Combining revisions

When corrections come from several files or reviewers:

- freeze the source and layout revisions before collecting decisions;
- keep scan evidence, editorial defaults, open readings and exact character positions distinct;
- apply decisions into a fresh revision, never in place;
- reconcile any two decisions that touch the same position against the scan;
- check deleted runs and moved positions explicitly, then render and compare text and page geometry again.

A receipt shows which files were used. A visual comparison shows only what was actually looked at.
