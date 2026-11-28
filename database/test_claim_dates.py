import unittest
from claim_dates import check_date, ganji, recorded_date
class DatePrecisionTests(unittest.TestCase):
    def test_only_complete_components(self):
        self.assertEqual(recorded_date('高廟丙寅一八六六年十二月二'),('1866-12','month',False))
        self.assertEqual(recorded_date('丙寅一八六六年閏五月廿六日卒'),('1866-05-26','day',True))
        self.assertEqual(recorded_date('辛巳一九四一年六月二十日生'),('1941-06-20','day',False))
        self.assertEqual(recorded_date('庚申十二月初二日卒'),(None,None,None))

    def test_three_digit_year_is_kept_as_written(self):
        # Some genealogies record years before 1000; check_date decides whether to doubt one.
        self.assertEqual(recorded_date('九五八年二月三日生'),('0958-02-03','day',False))


class CheckDateTests(unittest.TestCase):
    def test_ganji(self):
        self.assertEqual([ganji(y) for y in (1592, 1804, 1903, 1958)], ['壬辰', '甲子', '癸卯', '戊戌'])

    def test_clean_statements(self):
        self.assertEqual(check_date('高廟癸卯一九〇三年十一月十四日生'), ('birth', []))
        self.assertEqual(check_date('戊戌一九五八年十二月三日卒'), ('death', []))

    def test_dropped_one(self):
        # 戊戌 is 1958's label; 958's is 戊午.
        self.assertEqual(check_date('戊戌九五八年十二月三日卒'), ('death', ['dropped-leading-one']))

    def test_genuine_early_year(self):
        self.assertEqual(check_date('戊午九五八年生'), ('birth', []))

    def test_cut_at_a_page_break(self):
        # The run after the break: no leading 一, and the 卒 is in the next run.
        self.assertEqual(check_date('九四六年七月二日'), (None, ['short-year-unconfirmed', 'no-event-marker']))

    def test_cycle_mismatch(self):
        self.assertEqual(check_date('己巳一九○五年生'), ('birth', ['cycle-mismatch']))
        self.assertEqual(check_date('甲子九五八年生'), ('birth', ['cycle-mismatch']))

    def test_year_length(self):
        self.assertEqual(check_date('五八年生'), ('birth', ['year-length']))

    def test_cycle_label_alone(self):
        self.assertEqual(check_date('乙丑生'), ('birth', []))
