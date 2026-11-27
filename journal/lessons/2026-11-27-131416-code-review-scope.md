# An automated code review failed because its scope was too wide

Appendix item: 24. Date: 24 November 2026 (JST).

Terms used here:

- A **skill** is a packaged set of instructions for the coding assistant. `ce-code-review` is a skill that reviews a set of code changes.
- **Unstaged files** are changed files in the working folder that have not been selected for the next saved version (commit).

## Summary

An attempt to run the `ce-code-review` skill returned `status: failed`. Its scope included unrelated, older unstaged plans, research notes and a binary file, as well as the files actually selected for review.

## Impact

No completed review receipt exists for that stage. The record says so plainly instead of claiming a review.

## How it was noticed

The skill reported the failure.

## Root cause

The working folder held unrelated changes from other work. The review tool looked at the whole working folder, not only the selected files.

## Fix

The run record states "Code review: skipped" for that checkout. A separate independent review of the reference set and evaluator was completed, and its findings were fixed. A local scan of the changes and the test suite supplemented it.

## Lesson

Keep unrelated work out of the folder you review, for example by saving or moving it first, or by reviewing in a separate copy of the repository.

When a check fails, record that it did not run. Do not count it as passed.

## Evidence

- The run record for reference expansion, section "Review and correction".
