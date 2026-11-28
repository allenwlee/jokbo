"""Golden cases: text printed in the 1989 Anseong Lee jokbo, Jangsu branch, for men
born before 1920, with the runs a vision reader returned for it. Courtesy names are
left out. Every case was checked against the scan on 28 November 2026 (JST)."""
import unittest

from claim_dates import recorded_date
from entry_columns import date_statements, join_runs, runs_for, short_columns, usual_length

# p. 39: two lone 一 skipped inside full columns. One was in 十一月, which left a valid month.
P39_PRINTED = ['高廟癸卯一九〇三', '年十一月十四日生', '戊戌一九五八年十', '二月三日卒○墓長']
P39_READ = [['高廟癸卯', '九○三'], ['年十', '月十四', '日生'], ['戊戌', '九五八年十'], ['二月三日卒○墓長']]

# pp. 69-70: a death year split across a page break, 丙戌一 | 九四六年.
P70_RUNS = ['甲寅一九一四年六', '月三十日生丙戌一', '九四六年七月二日', '卒○墓溪内面明德', '里']

# pp. 73-74: the same across a page break, and the date closes with 卒, not 生.
P74_RUNS = ['高廟丁卯一', '八六七年生己酉一', '九六九年五月八日', '卒○墓']

# pp. 44-45: a birth year split across the gutter, 甲子一 | 八〇四年.
P45_RUNS = ['通政甲子一', '八〇四年五月十八', '日生己丑一八二九', '年正月十九日卒']


def facts(runs):
    text, _ = join_runs(enumerate(runs))
    return [(event, recorded_date(s)[0], problems) for _, _, s, event, problems in date_statements(text)]


class GridTests(unittest.TestCase):
    def test_printed_columns_fit_the_grid(self):
        self.assertEqual(usual_length(P39_PRINTED), 8)
        self.assertEqual(short_columns(P39_PRINTED), [])

    def test_skipped_characters_shorten_their_columns(self):
        read = [''.join(c) for c in P39_READ]
        self.assertEqual(short_columns(read, 8), [0, 1, 2])

    def test_short_last_column_is_allowed(self):
        self.assertEqual(short_columns(['卒○墓溪内面明德', '里'], 8), [])
        self.assertEqual(short_columns(['卒○墓溪内面明德', '里一二三四五六七八'], 8), [1])


class JoinedDateTests(unittest.TestCase):
    def test_reader_output_is_flagged_not_stored(self):
        read = [r for column in P39_READ for r in column]
        self.assertEqual(facts(read), [('birth', None, ['year-not-four-digits']),
                                       ('death', None, ['year-not-four-digits'])])

    def test_printed_text(self):
        self.assertEqual(facts(P39_PRINTED), [('birth', '1903-11-14', []), ('death', '1958-12-03', [])])

    def test_split_dates_join_whole(self):
        self.assertEqual(facts(P70_RUNS), [('birth', '1914-06-30', []), ('death', '1946-07-02', [])])
        self.assertEqual(facts(P74_RUNS), [('birth', '1867', []), ('death', '1969-05-08', [])])
        self.assertEqual(facts(P45_RUNS), [('birth', '1804-05-18', []), ('death', '1829-01-19', [])])

    def test_one_run_at_a_time_loses_the_year(self):
        self.assertEqual(facts(P70_RUNS[2:3]), [(None, None, ['year-not-four-digits', 'no-event-marker'])])

    def test_fact_maps_back_to_every_run_it_covers(self):
        text, spans = join_runs(enumerate(P70_RUNS))
        start, end, *_ = date_statements(text)[1]
        self.assertEqual(runs_for(spans, start, end), [(1, 5, 8), (2, 0, 8), (3, 0, 1)])


if __name__ == '__main__':
    unittest.main()
