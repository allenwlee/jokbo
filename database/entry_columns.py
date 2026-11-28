"""Join an entry's text runs into one reading-order string, and check columns
against the book's printed grid.

A jokbo entry is set in fixed-length columns, read top to bottom and right to
left, and it can continue across a column, the gutter or a page. A date often
breaks there: 丙戌一 | 九四六年七月二日卒. Extracting facts from one run at a
time cuts the year to 九四六 (946). Join the runs first, extract from the joined
text, and map each fact back to every run it covers with ``runs_for``.

A reader that skips a character shortens its column. In the book this module was
built on, every full column of entry text held the same number of characters
(8 on the chart pages checked), so a shorter column that is not an entry's last
is a missing character: 高廟癸卯 + 九○三 is 7, where the page prints
高廟癸卯一九〇三.
"""
import re
from collections import Counter

from claim_dates import check_date


def join_runs(runs):
    """runs: [(run_id, text)] in reading order. Returns (text, spans), where spans
    is [(run_id, start, end)] giving each run's place in the joined text."""
    spans, parts, at = [], [], 0
    for run_id, text in runs:
        spans.append((run_id, at, at + len(text)))
        parts.append(text)
        at += len(text)
    return ''.join(parts), spans


def runs_for(spans, start, end):
    """The runs a joined-text span [start, end) covers, as [(run_id, local_start, local_end)]."""
    return [(rid, max(start, s) - s, min(end, e) - s) for rid, s, e in spans if s < end and start < e]


def usual_length(columns):
    """The most common column length: the grid, when the caller does not know it."""
    return Counter(len(c) for c in columns).most_common(1)[0][0]


def short_columns(columns, cells=None):
    """columns: an entry's full printed columns in reading order, each the joined text
    of the runs the reader returned for it. Returns the indexes of columns whose length
    breaks the grid: any column but the last that is not exactly ``cells`` long, and a
    last column longer than ``cells``."""
    cells = cells or usual_length(columns)
    last = len(columns) - 1
    return [i for i, c in enumerate(columns) if (len(c) != cells if i < last else len(c) > cells)]


STATEMENT = re.compile(r'[^生卒]*[生卒]|[^生卒]+')


def date_statements(text):
    """Split joined entry text after each closing 生 or 卒 and check every piece that
    holds a year, including a dated tail with no closing marker. Returns
    [(start, end, statement, event, problems)]. A name or word containing 生 or 卒
    also splits the text, so read flagged statements in context."""
    out = []
    for m in STATEMENT.finditer(text):
        if '年' in m[0]:
            event, problems = check_date(m[0])
            out.append((m.start(), m.end(), m[0], event, problems))
    return out
