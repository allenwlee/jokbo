# Editorial review

Editorial review decides what the edition prints when the scan, the OCR and the models do not settle a reading on their own. It comes after [glyph review](transcription-and-glyph-review.md) and before rendering. The aim is a reading that someone else can check: every decision keeps its crop, its location, the evidence used and the basis of the choice.

## The procedure

1. **Identify the character from the original first.** Compare clear printings of the same character at their scan positions, including the surrounding text and the stroke that separates the candidates. Only then look at what the models said.
2. **Bind verified locations to one reading.** Once the scan shows that several locations hold the same character, every one of them gets the same Unicode value in the layout, the PDF and the database.
3. **Record conflicts.** Any OCR or model answer that differs from the verified reading is a conflict, even when it matches the draft, matches another model, or comes from the same model that read a clear example correctly. Keep the raw answers.
4. **Leave unclear locations open.** A blurred, misplaced or too-short crop stays unresolved until better evidence appears.
5. **Change a decision only on new source evidence,** and record the reason. If a layout revision moves a run, check its position again.
6. **Check the final output.** Before database import, compare the rendered and copied characters against the verified readings.

## Learn the book's conventions before reading in context

At the start of each book, read its front matter and a few representative pages from each kind of layout. Write down which conventions the book uses, where they apply, and one clear printed example of each:

- reading direction, and where it changes;
- generation labels and the generation-name chart, if there is one;
- the order of an entry: name, courtesy name, dates, spouse, burial;
- date formulas: sexagenary-cycle years (the 60-year cycle such as 甲子, 乙丑), reign years, numbered years, month and day;
- burial formulas and compass bearings;
- name annotations such as 一名 (alternate name);
- how a chart cell points to another page.

A book may have no Hangul readings, use several calendars, or change chart layout between sections. Use a convention only in the sections where the book shows it.

## Questions to ask about a disputed reading

The examples come from the Lee book unless marked as from the practice book.

| Question | Evidence to collect from your book | Example |
|---|---|---|
| What does this number label? | The grid lines, the row or column headings, neighbouring generations and the complete number. For a page reference, follow it and check that the target names the same person and points back. Use sibling order as a clue only where the book's ordering convention is established. | Practice book: the index reference `一一一` has three identical strokes stacked; a reader that drops one gives `一一`. In the Lee book, a return reference and the spacing told a three-digit page reference from a two-digit one. |
| What event belongs here? | The whole clause, continued across a column break if needed, and a clear parallel entry for the same event. | In one entry, `十三日卒○墓右同` puts `卒` ("died") between the day and the burial note. `辛` is also legitimate in cycle-year dates, so the position decides. |
| Does the full date limit the reading? | The whole year designation, the numbered year if printed, month, day and event marker, in the date order the section uses. Keep the calendar as recorded. | `甲戌` is a valid cycle year; `甲戊` is not. The same check helps with `己/巳`. In one entry the expected formula is `十月二日生`, but the print has `十日二日生`: transcribe `日` as printed and keep any interpretation of the date separate. `正月三日生` separates `正` from `生`. |
| Is the word printed more clearly somewhere else? | The full clan or place name in the title, headings and other entries of the same edition. Allow for historical spellings. | The book's title supports `安城` over `安成` in an entry. A printed address supplies context for `서울` over `서을`. |
| Does the name follow a generation pattern? | The branch, generation, prescribed character and its position from the book's own generation chart. Check whether the name is a primary or alternate name, and look for another printing. | The generation-name chart (行列表) on p. 4 helps judge `圭/桂/珪` and `燮/變`. Where `一名` introduces an alternate name, the pattern alone cannot settle the spelling. |
| Is the name printed in a second script or at a larger size? | The full Hanja name with its Hangul reading, if printed. Follow the index to the full entry and confirm it is the same person. Look at the distinguishing stroke, or the final Hangul consonant, at the larger size. | On p. 43, `默` in `相默` and the printed final ㄱ of 상묵 support 상묵 over 상무. On p. 38 the larger `㦥燮` shows 忄 and the reading 헌섭, settling `㦥` over `幰`. Practice book: `明德` is printed with its reading 명덕. |
| Could both readings be valid here? | Identify the field first, then narrow the candidates. If both make sense, compare clear printings or leave it open. | For `西/酉`, only `酉` fits the branch position of a cycle year. In a burial description ending in `坐`, `酉` can also be a compass bearing. Keep both until the print decides. |

If the print clearly breaks an expected formula, transcribe the print and flag the inconsistency. Do not correct the book.

## Edition-specific defaults

Some choices cannot be made from the glyph, because the typeface does not distinguish two Unicode encodings of the same character. The edition then needs a written default, applied only within that edition.

Worked example from the Lee book: the Hanja 진 is printed in a form that maps to either `鎭` or `鎮`. The edition transcribes `鎭` throughout unless a specific impression clearly shows `鎮`. An indistinct instance gets `鎭`, labelled as an editorial default rather than a scan reading. A clear contrary printing gets a location-specific exception; model output alone cannot create one. Where the scan clearly showed a different character in one name, the scan reading replaced the default for that location.

Put a default like this in two places:

- the book's configuration (`[editorial]` in the book-config file, see [book configuration](book-config.md)), so the decision travels with the book and any script or agent that applies it reads one value;
- the edition's editorial notes, so a reader of the PDF or database knows the reading is a convention and not a claim about the print.

Keep three things separate in the records: readings verified on the scan, readings set by a default, and readings still open. The review ledger stores verified and default readings in separate fields for this reason.

Circles get the same treatment. The Lee printer used circles as zeros, as separators and as placeholders for unknown name characters. Record each circle's role and encode it consistently: `〇` (U+3007) for a numeral, `○` (U+25CB) for a mark.

## Checking the printed book

A physical copy can settle what a scan cannot. Record who checked it, what they saw and what they chose, and keep the scan crop beside the note. In the Lee project the maintainer checked the printed book and selected `郞` for one title with a note on `郎/郞`, selected `闌` with a note that its interior resembles `東`, and read `彔` in one entry. In another entry the print appears to overlap `父` with a second character; that cause is unconfirmed and the proof reading there is marked tentative.

## Record for each decision

- the original crop and its location (opening, run, character offset);
- the parallel passage, rule or physical-book check used;
- the reading chosen and its basis: scan, editorial default, or physical book;
- the conflicting answers, with their source (OCR, model and run);
- what would reopen it.

## Testing this procedure on a second book

When you adapt this guide, test it on a book whose layout differs, or that lacks a convention this one relies on, such as a book with no generation-name chart. A careful reviewer, human or agent, should notice the missing evidence, use another source in the book, or leave the reading open.
