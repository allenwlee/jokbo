# Years lose their leading 一

Appendix item: 36. Date: 28 November 2026 (JST).

Terms used here:

- The book writes years with Hanja numerals: 1903 is 一九〇三. The leading 一 (one) is a single horizontal stroke.
- A **cycle-year label** (ganji, 干支) names a year in the 60-year cycle, such as 癸卯 for 1903 and 戊戌 for 1958. The book usually prints it right before the year, so the two check each other.
- A **layout run** is one stretch of text as the reader returned it, with its position. An entry's text is usually several runs.
- An entry ends a date with 生 (born) or 卒 (died).

## Summary

A query for birth years found years such as 0958 and 0903 in the database. Nine fact records, on seven printed pages, had a three-digit year. In every case the book prints a four-digit year starting with 一. Each one was checked against the scan.

The 一 was lost in two different ways.

**The date crosses a break.** Six of the records are dates that start at the foot of one column and continue at the top of the next. Sometimes the next column is across the gutter or on the next page. The last character before the break is the year's 一:

```
p. 69, last column      月三十日生丙戌一
p. 70, first column     九四六年七月二日
                        卒○墓溪内面明德
```

The fact extraction quoted only the run after the break, 九四六年七月二日. The date reader then stored the year as 0946. The same happened on p. 74 (己酉一 | 九六九年, 1969), across the gutter between pp. 44 and 45 (甲子一 | 八〇四年, 1804), and at an ordinary column break on one more page. The 一 was in the data, in the run before the break.

**The reader skipped a lone 一.** On p. 39 the book prints, in full columns of eight characters:

```
高廟癸卯一九〇三
年十一月十四日生
戊戌一九五八年十
二月三日卒○墓長
```

The vision reader returned 高廟癸卯 and 九○三 as two runs with nothing between them, and 年十 and 月十四 the same way. It dropped three separate 一. The one in 十一月 (November) turned the birth date into 十月 (October). That month is valid, so no date check could have caught it. One more mid-column drop of this kind was found on another page.

The same nine records had two more kinds of error:

- **Deaths stored as births.** On pp. 70 and 74 the split dates close with 卒, but four records stored them as births.
- **Facts on the wrong appearance.** The p. 45 date was attached to the man's wife. The pp. 70 and 74 dates were attached to three appearances whose only "name" was a generation label such as 二十四世 ("24th generation"). One of those label appearances had collected twelve birth claims and two death dates from a whole column of entries.

## Impact

A year of 0958 put a person a thousand years too early. The privacy register treats any year that is not four digits as unverified, so it kept these appearances restricted. That was safe, but it also kept back people who were born before 1920.

A dropped 一 inside a month or day gives a wrong date that looks right. Only the p. 39 month error was found, and only because the year on the same line was wrong too.

Facts on the wrong appearance give a birth or death to the wrong person. Facts on a generation label give them to nobody.

## How it was noticed

A database query for birth years turned up years starting with 0. Following each fact's source passage back to its layout runs showed whether a 一 sat at the end of the run before. Enlarged crops of the scan settled each case. For the first case, the explanation was "a column break". The maintainer pointed out that on p. 39 the 一 was there in the middle of the column. That showed the second cause.

## Root cause

- The fact extraction worked on one layout run at a time. A date is one statement, but a column or page break cuts it into several runs.
- The date reader accepted a three- or four-digit year and padded the short ones with a zero. A three-digit year can never be right in a book whose dates run from 1592 to the 1980s.
- A lone 一 is one thin stroke. The reader read it as a rule line or a speck and dropped it, as it had in index references and generation labels (see [small strokes](2026-11-27-131407-small-strokes-circles-and-digits-drop-out.md)).
- The fact type came from the model's label, not from the 生 or 卒 that closes the date.
- Nothing stopped a generation label from becoming an appearance.

## Fix

- `database/claim_dates.py` now accepts only four-digit years. A three-digit year gives no date, so it is flagged instead of stored as 0958. A new `check_date` reports, for one date statement:
  - `year-not-four-digits`;
  - `cycle-mismatch` (a cycle-year label that is not the year's);
  - `no-event-marker`.

  It also returns `birth` or `death` from the closing 生 or 卒.
- `database/entry_columns.py` joins an entry's runs in reading order before dates are read. `date_statements` reads each date from the joined text, and `runs_for` maps it back to every run it covers. `short_columns` flags any column that is not the grid's length, except an entry's last.
- `database/test_entry_columns.py` keeps four of the cases above as golden cases. Each holds the printed text, what the reader returned, and the correct dates. A change to the reader or the extraction should pass them first.

At the time of writing, the nine records had been identified and their correct values checked against the scan. They had not yet been corrected in the database. The new checks had not yet been run over the whole book.

## Lesson

Read facts from an entry's joined text, never from one run. Column, gutter and page breaks fall in the middle of dates.

Use the book's own redundancy:

- A full column has a fixed number of characters, so a short one is missing something.
- A cycle-year label has to match its year.
- 生 or 卒 says which event a date is.

Each of these is a free, model-independent check.

A three-digit year is a reading error, not a date. Reject it at import rather than padding it.

Count what the checks cannot see. A dropped stroke that leaves a valid month passes every date check. Only the column count catches it.

## Evidence

- The 28 November database audit of three-digit years: the nine fact records, their source passages and layout runs, and enlarged scan crops of each case.
- The layout's run lengths. Among body-text runs of seven to ten characters, eight is by far the most common length. Some pages also have nine-character columns, so the grid has to be measured per page or section, not assumed.
