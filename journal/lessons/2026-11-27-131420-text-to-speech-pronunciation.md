# Text-to-speech mispronounced a place name

Appendix item: 32. Date: 25 November 2026 (JST).

Terms used here:

- **Text-to-speech** (TTS) turns a script into spoken audio. The history video used OpenAI `gpt-4o-mini-tts` with the voice `cedar`.
- **Transcribe-back** means turning the generated audio back into text with a speech-recognition model, then comparing that text with the script.

## Summary

The video narration is in English with Korean names written in Hangul, so the voice says them in Korean. In one recording, 장수 (Jangsu, the branch's home county) came out sounding like "Cheongju", a different city.

## Impact

A wrong place name in a history video teaches the wrong history. A listener cannot tell it is a machine error.

## How it was noticed

The recording was transcribed back and compared with the script line.

## Root cause

TTS models guess pronunciation and do not always say the same text the same way. A short Hangul word in an English sentence is easy to misread.

## Fix

Every scene's recording is transcribed back with OpenAI `whisper-1` and compared with the script. A line that comes out wrong is recorded again, up to three extra attempts per line. The same transcription also gives the start time of each spoken word, which sets when name cards and map markers appear.

The end card of each video states that the narration is an AI-generated voice.

## Lesson

Do not trust generated speech by listening once. Check it automatically against the script, with a fixed retry limit, and keep the check's result with the audio.

## Evidence

- The history video folder's README, "How the video was made".
