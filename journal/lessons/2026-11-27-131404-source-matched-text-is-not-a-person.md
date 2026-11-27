# Text that matches the source can still mean the wrong thing

Appendix items: 5, 25. Date: 24 November 2026 (JST).

Terms used here:

- **Hanja** are the Chinese characters used in Korean writing. **Hangul** is the Korean alphabet. The book often prints a name in Hanja with its Hangul reading beside it.
- A **courtesy name** is an adult alternative name. The book introduces it with 字.
- An **exact-substring check** confirms that every piece of text a model quotes really occurs in the digitized page.
- An **entry** is one person's block of text in the book. A **fact** is one statement extracted from it, such as a birth date.

## Summary

Two stages passed their mechanical checks while producing wrong meaning.

In the person calibration, eight model requests tried to list the people on sample openings. Every returned name passed the exact-substring check, with zero errors. The outputs still counted courtesy names, names on the index pages, and both halves of a Hanja/Hangul pair as separate people. One response listed 相淳 and its printed reading 상순 as two different chart subjects.

In the later page-extraction trial on six pages, the importer flagged 17 quotes that could not be aligned with the source and 7 facts that crossed a proposed entry boundary. The model also labeled some births as `birth_date` instead of `birth`, which hid those dates from date queries. On one manually mapped sample page, the model proposed all 10 child-to-parent links in the reference. Eight parent choices matched and two did not.

## Impact

Had the calibration output been imported, the database would have held more "people" than the book contains.

Facts attached to the wrong entry give a birth or a parent to the wrong person.

Dates under the wrong label would have been missing from every date search.

## How it was noticed

The calibration responses were read by hand against the page. Their validation field was empty in each case, which is how the gap between "found in the text" and "is a person" became clear.

In the extraction trial, the importer's issue list reported the alignment and boundary failures. Review of the imported facts found the label defect. Comparing with the manual reference for the sample page found the two wrong parent choices.

## Root cause

An exact-substring check tests where text is. It does not test what the text is: a person's name, a courtesy name, an index reference, or another script's form of the same name.

The importer accepted the model's labels as given and had no rule to normalize them.

## Fix

No model-generated people from the calibration were imported. The first candidates came from fixed, written rules instead, and every candidate was marked unreviewed.

The importer now normalizes birth and death labels. It can recover a quote when exactly one matching span exists in the proposed owner's entry and that span overlaps the model's citation. On replay of the same six responses, it recovered 13 citations and accepted 188 facts instead of 175. The number of non-empty birth dates in the sample rose from 10 to 65.

The importer now challenges a parent choice that falls outside the preceding-row interval, and a father statement that appears after a spouse marker. Across the six pages, 56 links passed the revised checks. Every rejection stays in the issue list.

Printed claims and family-supplied claims are stored separately. For example, a family member supplied a birth year two years earlier than the printed one. Both are kept as separate claims about the same appearance. Neither erases the other, and a query has to choose between them or show both instead of counting two people.

## Lesson

Treat a source-matched result as a candidate appearance, not a verified person.

Before scaling a model or a rule, freeze a reviewed sample that includes the hard page types. Measure both false people and missed people against it. A clean JSON parse, an exact substring match, model confidence and model agreement do not replace that test.

Normalize labels before import, and keep a list of every rejected proposal.

## Evidence

- The run record for the person-appearance candidate stage, including its calibration section.
- The internal solution note "Exact substring checks do not validate genealogy person extraction".
- The run records for the page-extraction calibration and for the accuracy check before full-book processing.
- The run record for the manually mapped sample page, which describes keeping printed and family-supplied birth claims separate.
