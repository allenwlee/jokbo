"""Read explicit year/month/day precision from a literal Hanja date statement,
and say why a date quote cannot be trusted as written."""
import re

DIGITS = str.maketrans('〇○零一二三四五六七八九','000123456789')
YEAR = re.compile(r'(?<![0-9])([0-9]{3,4})年')
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
    """A three-digit year is kept as written (958 -> '0958'): some genealogies really
    record years before 1000. check_date says whether it is more likely a dropped 一."""
    text=quote.translate(DIGITS)
    years=list(YEAR.finditer(text))
    if len(years)!=1:return None,None,None
    year=years[0]
    date=year[1].zfill(4)
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
    problems lists reasons to re-read the source before trusting the date:
      dropped-leading-one     a three-digit year whose cycle-year label fits the year
                              plus 1000, not the year itself: 戊戌九五八 is 1958 (戊戌),
                              not 958 (戊午)
      short-year-unconfirmed  a three-digit year with no cycle-year label to confirm it.
                              Early ancestors can have such years, so this is a prompt
                              to check the scan and the column, not a rejection
      year-length             a year of one, two, or five or more numerals
      cycle-mismatch          a cycle-year label that fits neither reading of the year
      no-event-marker         no closing 生 or 卒, so the fact type is a guess
    A statement with no problems can still be wrong: a dropped 一 in 十一月 leaves a
    valid month. Only a column-length check sees that.
    """
    text = quote.translate(DIGITS)
    problems = []
    years = [m[1] for m in ANY_YEAR.finditer(text)]
    labels = ganji_pairs(quote)
    if any(len(y) not in (3, 4) for y in years):
        problems.append('year-length')
    year = next((int(y) for y in years if len(y) in (3, 4)), None)
    if year is not None and year < 1000:
        if labels and all(p == ganji(year + 1000) for p in labels):
            problems.append('dropped-leading-one')
        elif not labels:
            problems.append('short-year-unconfirmed')
        elif any(p != ganji(year) for p in labels):
            problems.append('cycle-mismatch')
    elif year is not None and any(p != ganji(year) for p in labels):
        problems.append('cycle-mismatch')
    markers = [c for c in quote if c in EVENTS]
    if not markers:
        problems.append('no-event-marker')
    return (EVENTS[markers[-1]] if markers else None), problems
