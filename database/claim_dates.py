"""Read explicit year/month/day precision from a literal Hanja date statement,
and say why a date quote cannot be trusted as written."""
import re

DIGITS = str.maketrans('〇○零一二三四五六七八九','000123456789')
YEAR = re.compile(r'(?<![0-9])([0-9]{4})年')
ANY_YEAR = re.compile(r'(?<![0-9])([0-9]+)年')
MONTH = re.compile(r'(閏)?(正|元|冬|臘|[0-9十廿]{1,3})月')
DAY = re.compile(r'(初?[0-9十廿卅]{1,4})日')
STEMS = '甲乙丙丁戊己庚辛壬癸'
BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
EVENTS = {'生': 'birth', '卒': 'death'}


def ganji(year):
    """The sexagenary (cycle-year) label of a common-era year, e.g. 1958 -> 戊戌."""
    n = (year - 4) % 60
    return STEMS[n % 10] + BRANCHES[n % 12]


def ganji_pairs(text):
    return [text[i:i + 2] for i in range(len(text) - 1) if text[i] in STEMS and text[i + 1] in BRANCHES]


def integer(s):
    s=s.removeprefix('初').replace('廿','2十').replace('卅','3十')
    if s in ('正','元'): return 1
    if s in ('冬','臘'): return {'冬':11,'臘':12}[s]
    if s.count('十')==1:
        tens,ones=s.split('十')
        if len(tens)>1 or len(ones)>1:return None
        return int(tens or 1)*10+int(ones or 0)
    return int(s) if s.isdecimal() else None


def recorded_date(quote):
    """Only a four-digit year is a year: a three-digit one is a dropped 一, not a date."""
    text=quote.translate(DIGITS)
    years=list(YEAR.finditer(text))
    if len(years)!=1:return None,None,None
    year=years[0]
    date=year[1]
    after=text[year.end():]
    month=MONTH.match(after)
    if not month:return date,'year',None
    m=integer(month[2])
    if not m or m>12:return date,'year',None
    date+=f'-{m:02}'
    day=DAY.match(after[month.end():])
    if not day:return date,'month',bool(month[1])
    d=integer(day[1])
    if not d or d>31:return date,'month',bool(month[1])
    return date+f'-{d:02}','day',bool(month[1])


def check_date(quote):
    """Check one date statement as written. Returns (event, problems).

    event is 'birth' or 'death' from the statement's closing 生 or 卒, or None.
    problems lists reasons to re-read the source before storing the date:
      year-not-four-digits  a year of 1-3 or 5+ numerals (a dropped or extra stroke,
                            or a date cut at a column or page break)
      cycle-mismatch        a cycle-year label that is not the label of the year
      no-event-marker       no closing 生 or 卒, so the fact type is a guess
    A statement whose problems list is empty can still be wrong: a dropped 一 in
    十一月 leaves a valid month. Only a column-length check sees that.
    """
    text = quote.translate(DIGITS)
    problems = []
    years = [m[1] for m in ANY_YEAR.finditer(text)]
    if any(len(y) != 4 for y in years):
        problems.append('year-not-four-digits')
    full = [int(y) for y in years if len(y) == 4]
    if full and any(p != ganji(full[0]) for p in ganji_pairs(quote)):
        problems.append('cycle-mismatch')
    markers = [c for c in quote if c in EVENTS]
    if not markers:
        problems.append('no-event-marker')
    return (EVENTS[markers[-1]] if markers else None), problems
