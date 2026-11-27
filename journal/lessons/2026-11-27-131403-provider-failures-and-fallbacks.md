# Provider failures: credits, timeouts and rate limits

Appendix items: 4, 9. Dates: 20–24 November 2026 (JST).

Terms used here:

- A **provider** is the company that actually runs a model. **OpenRouter** is a service that sends one kind of request to many models and providers.
- **In-session vision** means the coding assistant looked at images inside the working conversation, instead of calling a separate model API.
- A **rate limit** is a provider refusing more requests for a while.

## Summary

Several outside services failed during the project.

During the first small pilot, a call to the OpenAI Responses API with `gpt-5-mini` returned an "insufficient credits" error. The targeted follow-up readings were then done with in-session vision. Later vision calls went through OpenRouter.

In the full-page audit on 20 November, 16 page responses timed out or failed to parse. Gemini 2.5 Flash recovered them.

On 23 November, Google AI Studio rate limits stopped Gemini 2.5 Flash-Lite after 312 of 1,708 crop boards. Qwen3-VL 235B read the other 1,396.

In a small parallel trial, six workers sent six jobs. Four hit rate limits and used up their three attempts.

## Impact

No data was lost. The costs were small.

The in-session readings left no API receipt. Their model, version and token use were never recorded.

Because the full crop pass switched models partway, each board was read by one model only. The two models covered different boards, so the pass gives no agreement between models.

The incomplete parallel trial could not support any claim that parallel work was faster.

## How it was noticed

The services returned error messages. The response ledgers marked timeouts and parse failures. The adaptive runner logged its worker count dropping from five to one.

## Root cause

Account limits and provider capacity are outside the project's control. Long structured answers can be cut off or malformed, which shows up as a parse failure.

## Fix

Vision calls moved to OpenRouter, so one request format could reach several models.

The saved crop-reading script uses an 80-second timeout, up to three attempts, and waits of 1, 2 and 4 seconds between attempts. It caches each response by a fingerprint (SHA-256) of the request. It rejects answers with missing, duplicate or unexpected crop IDs and rejects truncated output.

In the whole-book database edition, malformed or truncated answers were sent again in numbered retry passes: 28 requests in the first retry and 4 in the last.

## Lesson

Expect outside services to fail. Make retries bounded and logged.

Record failed attempts with the provider and model, not only the successes.

If a pass has to switch models, say so in the results. Do not report it as two-model agreement.

A spending target written in a run note is not a spending limit. In the 23 November trials, a US$1 target was recorded in advance, but the runner did not enforce a dollar ceiling. A real cap has to be in code.

## Evidence

- The notes collected in the draft open-source plan (the `gpt-5-mini` credits error and the move to OpenRouter).
- The character audit and the technical workflow record, section 2, on the 16 recovered responses.
- The conversion work log entries for 23 November: "Review tooling trial" and "Full crop-reading pass".
- The technical workflow record, section 4, for the script's retry and validation settings.
- The whole-book run record and the edition's provider cost report, for the retry passes.
