# The video pipeline was tied to one machine

Appendix item: 33. Date: 25 November 2026 (JST).

Terms used here:

- A **pipeline** is the chain of scripts that makes an output, here narration and then video frames.
- A **hard-coded path** is a file location written directly into a script instead of passed in as a setting.

## Summary

The history-video scripts were written for one machine. They read and write fixed folders under `/tmp/`.

The retry and fix scripts did not call shared functions. They opened an older script's source, cut off part of it, and ran the rest with Python's `exec()`. Each fix script was a near copy of the last.

The narration script read its API key from a secrets file in the home folder.

## Impact

Nobody else can rebuild the video without recreating the same folders. A change to the main script can silently break the fix scripts, because they depend on where a particular line of text sits in its source.

## How it was noticed

Writing the rebuild instructions in the video folder's README made the fixed paths and copied scripts obvious.

## Root cause

The video was made quickly, one problem at a time. Each fix was patched onto the last instead of being folded back into the main script.

## Fix

At the time, the README documented the fixed paths and the exact rebuild steps instead of hiding them.

In this public repository's history-video method, the scripts read their folders, fonts and narration files from a configuration file (see `video-config.example.toml` there). API keys come from environment variables set in the shell. The copied fix scripts are not part of the method; they survive only as this lesson.

## Lesson

Pass input and output folders as arguments from the start. Read API keys from environment variables or a documented settings file, not a personal path.

When a fix works, move it into the main script as a function and delete the copy.

## Evidence

- The history video folder's README, "Rebuilding the videos".
- The retry and fix scripts in the video pipeline folder.
