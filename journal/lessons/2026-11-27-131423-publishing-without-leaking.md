# Publishing the methods without publishing the family

Appendix: not in the original 35 items. This lesson covers the publishing stage itself. Date: 27 November 2026 (JST).

Terms used here:

- **Git history** is every saved version of every file in a repository, not only the current files.
- An **allowlist** is a list of files that may leave. Anything not on the list stays private.
- A **privacy register** is a file that classes every person appearance in the book as `open` or `restricted`, with a reason.
- A **leak checker** scans the exported folder for personal data before anything is published.

## Summary

While planning the public repository, the maintainer and the coding assistant looked for every way personal data could leak. The project's privacy rule is simple to state: people born in 1920 or earlier may appear in full; everyone else may appear only as a short glyph or reading used to teach a lesson, with no page number, date or relatives. Applying it was not simple. The planning found these risks.

1. **The history contained the scans.** The scanned book was committed on the first day. By the time of planning, the history was about 218 MB and contained every scan and database export. Making the working repository public, even after deleting files, would have published all of it.
2. **"Tracked minus ignored" was not a safe list.** 48 tracked files match the repository's own ignore rules, and 18 tracked files carry the `.local.` marker meant for files that never leave the machine. They were committed before or despite those rules.
3. **Names repeat across the 1920 cutoff.** 24 distinct names of two or more characters belong both to an appearance dated 1920 or earlier and to one dated after 1920. 168 names belong to an open appearance and to at least one restricted appearance. A filter that works on name strings cannot apply the rule.
4. **Models misread modern years as old ones.** In one stored date, 九五八年 ("958") became the year 0958. The printed year was most likely 1958, with the leading 一 lost. In another, 己巳一九○五年 pairs the cycle year 己巳, which falls in 1929 in this period, with the digits 1905. Taken at face value, both look like dates before 1920.
5. **Most people have no date.** Of 3,349 appearances, 1,862 have no dated claim and could not be placed from relatives. Another 122 were restricted through a relative dated after 1920. The family-tree links that might place them are model proposals that no one has reviewed.
6. **Names also appear in English letters.** Run records and notes wrote some modern family members' names in romanized form. A checker that looks only for Hanja and Hangul would miss them.
7. **Identity sits in places nobody reads.** Commits carry the maintainer's name and email. An archive of page readings lists a local account name as the owner of every member. A PDF's metadata names the scanner model. Test fixtures, prompts, run records and video scripts quote real entries. Some file and folder names point at a particular entry.

## Impact

None of this was published. Had the working repository been made public, it would have exposed living people's names, birth dates, relationships, photos and an address, and identified the maintainer.

## How it was noticed

A file-by-file inventory of the repository, a search for personal data outside the obvious places, and a first build of the privacy register on 27 November. The register's counts made the size of the undated and unverified groups clear.

## Root cause

The repository was built as a private family workspace. No privacy boundary existed when the first files were saved, and personal data spread into tests, logs and metadata as the work went on.

## Fix

- The working repository stays private with its full history. The public repository starts with fresh history.
- Only files on an explicit allowlist are exported. New files stay private until someone adds them. Ignore rules and tracking status are never consulted.
- The privacy register classes every appearance. An appearance is `open` only when every dated birth claim has a complete four-digit year of 1920 or earlier that agrees with any cycle year. Truncated or conflicting years are `date-unverified`. Undated, unplaceable appearances are restricted. At the 27 November build, 264 appearances were open and 3,085 restricted.
- Public text, including this journal, is rewritten by hand rather than redacted automatically. Every family-member name in it is tied, in an internal file that is never exported, to the exact appearance it refers to. That lets the checker tell an open ancestor from a restricted namesake.
- A leak checker is planned to scan the exported folder: names in Hanja, Hangul and romanized forms, years after 1920 near names, relation markers, identity strings, image and PDF metadata, and archive owner fields. Any finding fails the export.
- The maintainer is anonymous in public text.

### A second failure, found after the gate passed

The gate passed all three stages, and then a fresh agent, given only the exported files, followed the README's quickstart. Three of its seven steps failed with `cleaned scan does not match approved manifest`. The leak gate's metadata-strip step had rewritten every PDF in the export, including the practice book's clean scans. The practice book pins those scans by SHA-256, so the rewritten files no longer matched. The gate now strips a copy first and keeps the original bytes when stripping removes nothing. The tests in this repository had passed throughout, because they ran against the unstripped files. Only a run from the exported copy, by an agent with no other context, showed the problem.

## Lesson

Decide what is private before the first commit. Start a private project as if it might one day be public, or keep personal data in a separate store from the start.

Publish from an allowlist into a new repository. Do not try to clean a history that already contains the data.

Classify people, not names. In a genealogy, names repeat across generations.

Treat a date as unverified until its digits and its cycle year agree. Treat undated people as restricted unless something reviewed places them.

Search metadata, test fixtures, prompts, logs and file names, not only documents.

## Evidence

- The planning research for the public repository, which inventoried 268 files and listed personal data in non-obvious places.
- The privacy register's build receipt, with counts by reason, generated on 27 November 2026 at 13:07 JST.
- The repository's own commit history and ignore rules.
