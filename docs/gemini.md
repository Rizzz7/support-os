https://ai.google.dev/gemini-api/docs/troubleshooting

Use this guide to help you diagnose and resolve common issues that arise when
you call the Gemini API. You may encounter issues from either
the Gemini API backend service or the client SDKs. Our client SDKs are
open sourced in the following repositories:

- [python-genai](https://github.com/googleapis/python-genai)
- [js-genai](https://github.com/googleapis/js-genai)
- [go-genai](https://github.com/googleapis/go-genai)

If you encounter API key issues, verify that you have set up
your API key correctly per the [API key setup guide](https://ai.google.dev/gemini-api/docs/api-key).

## Gemini API backend service error codes

The following table lists common backend error codes you may encounter, along
with explanations for their causes and troubleshooting steps:

|---|---|---|---|---|
| **HTTP Code** | **Status** | **Description** | **Example** | **Solution** |
| 400 | INVALID_ARGUMENT | The request body is malformed. | There is a typo, or a missing required field in your request. | Check the [API reference](https://ai.google.dev/api) for request format, examples, and supported versions. Using features from a newer API version with an older endpoint can cause errors. |
| 400 | FAILED_PRECONDITION | Gemini API free tier is not available in your country. Please enable billing on your project in Google AI Studio. | You are making a request in a region where the free tier is not supported, and you have not enabled billing on your project in Google AI Studio. | To use the Gemini API, you will need to setup a paid plan using [Google AI Studio](https://aistudio.google.com/apikey). |
| 403 | PERMISSION_DENIED | Your API key doesn't have the required permissions. | You are using the wrong API key; you are trying to use a tuned model without going through [proper authentication](https://ai.google.dev/gemini-api/docs/model-tuning). | Check that your API key is set and has the right access. And make sure to go through proper authentication to use tuned models. |
| 404 | NOT_FOUND | The requested resource wasn't found. | An image, audio, or video file referenced in your request was not found. | Check if all [parameters in your request are valid](https://ai.google.dev/gemini-api/docs/troubleshooting#check-api) for your API version. |
| 429 | RESOURCE_EXHAUSTED | You've exceeded one of the API's rate limits (RPM, TPM, RPD, spend, etc.). | You are sending too many requests, using too many tokens, or exceeding spend-based limits for your account's billing history and tier. | Verify that you're within the model's [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits). Wait and retry after a short period. Reduce the rate or size of your requests. [Request a rate limit increase](https://ai.google.dev/gemini-api/docs/rate-limits#request-rate-limit-increase) if needed. |
| 499 | CANCELLED | The operation was cancelled, typically by the caller. | The client closed the connection before the API could finish responding. | Check if your client or network infrastructure is prematurely closing the connection (e.g., due to a client-side timeout). |
| 500 | INTERNAL | An unexpected error occurred on Google's side. | Your input context is too long. | Check the [Gemini API status page](https://aistudio.google.com/status) for any ongoing incidents. Reduce your input context or temporarily switch to another model (e.g. from Gemini 2.5 Pro to Gemini 2.5 Flash) and see if it works. Or wait a bit and retry your request. If the issue persists after retrying, please report it using the **Send feedback** button in Google AI Studio. |
| 503 | UNAVAILABLE | The service may be temporarily overloaded or down. | The service is temporarily running out of capacity. | Check the [Gemini API status page](https://aistudio.google.com/status) for any ongoing incidents. Temporarily switch to another model (e.g. from Gemini 2.5 Pro to Gemini 2.5 Flash) and see if it works. Or wait a bit and retry your request. If the issue persists after retrying, please report it using the **Send feedback** button in Google AI Studio. |
| 504 | DEADLINE_EXCEEDED | The service is unable to finish processing within the deadline. | Your prompt (or context) is too large to be processed in time. | Set a larger 'timeout' in your client request to avoid this error. |

## Check your API calls for model parameter errors

Verify that your model parameters are within the following values:

|---|---|
| **Model parameter** | **Values (range)** |
| Candidate count | 1-8 (integer) |
| Temperature | 0.0-1.0 |
| Max output tokens | Use the [models page](https://ai.google.dev/gemini-api/docs/models/gemini) to determine the maximum number of tokens for the model you are using. |
| TopP | 0.0-1.0 |

In addition to checking parameter values, make sure you're using the correct
[API version](https://ai.google.dev/gemini-api/docs/api-versions) (e.g., `/v1` or `/v1beta`) and
model that supports the features you need. For example, if a feature is in Beta
release, it will only be available in the `/v1beta` API version.

## Check if you have the right model

Verify that you are using a supported model listed on our [models
page](https://ai.google.dev/gemini-api/docs/models/gemini).

## Higher latency or token usage with 2.5 models

If you're observing higher latency or token usage with the 2.5 Flash and Pro
models, this can be because they come with **thinking is enabled by default** in
order to enhance quality. If you are prioritizing speed or need to minimize
costs, you can adjust or disable thinking.

Refer to [thinking page](https://ai.google.dev/gemini-api/docs/thinking#set-budget) for
guidance and sample code.

## Safety issues

If you see a prompt was blocked because of a safety setting in your API call,
review the prompt with respect to the filters you set in the API call.

If you see `BlockedReason.OTHER`, the query or response may violate the [terms
of service](https://ai.google.dev/terms) or be otherwise unsupported.

## Recitation issue

If you see the model stops generating output due to the RECITATION reason, this
means the model output may resemble certain data. To fix this, try to make
prompt / context as unique as possible and use a higher temperature.

> [!NOTE]
> The \`temperature\`, \`top_p\`, and \`top_k\` parameters control how the model generates responses. Although you can modify these parameters, we strongly recommend keeping them at their default values for Gemini 3.x models. Changing these parameters (for example, setting the temperature below 1.0) can cause unexpected behavior, such as looping or degraded performance, particularly in complex mathematical or reasoning tasks.

## Repetitive tokens issue

If you see repeated output tokens, try the following suggestions to help
reduce or eliminate them.

| Description | Cause | Suggested workaround |
| Repeated hyphens in Markdown tables | This can occur when the contents of the table are long as the model tries to create a visually aligned Markdown table. However, the alignment in Markdown is not necessary for correct rendering. | Add instructions in your prompt to give the model specific guidelines for generating Markdown tables. Provide examples that follow those guidelines. You can also try adjusting the temperature. For generating code or very structured output like Markdown tables, high temperature have shown to work better (\>= 0.8). The following is an example set of guidelines you can add to your prompt to prevent this issue: ``` # Markdown Table Format * Separator line: Markdown tables must include a separator line below the header row. The separator line must use only 3 hyphens per column, for example: |---|---|---|. Using more hypens like ---, ---, --- can result in errors. Always use |:---|, |---:|, or |---| in these separator strings. For example: | Date | Description | Attendees | |---|---|---| | 2024-10-26 | Annual Conference | 500 | | 2025-01-15 | Q1 Planning Session | 25 | * Alignment: Do not align columns. Always use |---|. For three columns, use |---|---|---| as the separator line. For four columns use |---|---|---|---| and so on. * Conciseness: Keep cell content brief and to the point. * Never pad column headers or other cells with lots of spaces to match with width of other content. Only a single space on each side is needed. For example, always do "| column name |" instead of "| column name                |". Extra spaces are wasteful. A markdown renderer will automatically take care displaying the content in a visually appealing form. ``` |
| Repeated tokens in Markdown tables | Similar to the repeated hyphens, this occurs when the model tries to visually align the contents of the table. The alignment in Markdown is not required for correct rendering. | - Try adding instructions like the following to your system prompt: ``` FOR TABLE HEADINGS, IMMEDIATELY ADD ' |' AFTER THE TABLE HEADING. ``` - Try adjusting the temperature. Higher temperatures (\>= 0.8) generally helps to eliminate repetitions or duplication in the output. |
| Repeated newlines (`\n`) in structured output | When the model input contains unicode or escape sequences like `\u` or `\t`, it can lead to repeated newlines. | - Check for and replace forbidden escape sequences with UTF-8 characters in your prompt. For example, `\u` escape sequence in your JSON examples can cause the model to use them in its output too. - Instruct the model on allowed escapes. Add a system instruction like this: ``` In quoted strings, the only allowed escape sequences are \\, \n, and \". Instead of \u escapes, use UTF-8. ``` |
| Repeated text in using structured output | When the model output has a different order for the fields than the defined structured schema, this can lead to repeating text. | - Don't specify the order of fields in your prompt. - Make all output fields required. |
| Repetitive tool calling | This can occur if the model loses the context of previous thoughts and/or call an unavailable endpoint that it's forced to. | Instruct the model to maintain state within its thought process. Add this to the end of your system instructions: ``` When thinking silently: ALWAYS start the thought with a brief (one sentence) recap of the current progress on the task. In particular, consider whether the task is already done. ``` |
| Repetitive text that's not part of structured output | This can occur if the model gets stuck on a request that it can't resolve. | - If thinking is turned on, avoid giving explicit orders for how to think through a problem in the instructions. Just ask for the final output. - Try a higher temperature \>= 0.8. - Add instructions like "Be concise", "Don't repeat yourself", or "Provide the answer once". |
|---|---|---|

## Blocked or non-working API keys

This section describes how to check whether your Gemini API key is blocked
and what to do about it.

### Understand why keys are blocked

We have identified a vulnerability where some API keys may have been publicly
exposed. To protect your data and prevent unauthorized access, we have
proactively blocked these known leaked keys from accessing the Gemini API.

### Confirm if your keys are affected

If your key is known to be leaked, you can no longer use that key with the
Gemini API. You can use [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-keys) to see if any of
your API keys are blocked from calling the Gemini API and generate new
keys. You may also see the following error returned when attempting to use
these keys:

    Your API key was reported as leaked. Please use another API key.

### Action for blocked API keys

You should generate new API keys for your Gemini API integrations using [Google
AI Studio](https://ai.google.dev/gemini-api/docs/api-keys). We strongly recommend reviewing your API
key management practices to ensure that your new keys are kept secure and are
not publicly exposed.

### Unexpected charges due to vulnerability

[Submit a billing support case](https://console.cloud.google.com/support/chat).
Our billing team is working on this, and we will communicate updates as soon as
possible.

### Google's security measures for leaked keys

**How is Google going to help secure my account from cost overrun and abuse if
my API keys are leaked?**

- We are moving towards issuing API keys when you request a new key using [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-keys) that will by default be limited to only Google AI Studio and not accept keys from other services. This will help prevent any unintended cross-key usage.
- We are defaulting to blocking API keys that are leaked and used with the Gemini API, helping prevent abuse of cost and your application data.
- You will be able to find the status of your API keys within [Google AI
  Studio](https://ai.google.dev/gemini-api/docs/api-keys) and we will work on communicating proactively when we identify your API keys are leaked for immediate action.

## Improve model output

For higher quality model outputs, explore writing more structured prompts. The
[prompt engineering guide](https://ai.google.dev/gemini-api/docs/prompting-strategies) page
introduces some basic concepts, strategies, and best practices to get you
started.

## Understand token limits

Read through our [Token guide](https://ai.google.dev/gemini-api/docs/tokens) to better understand how
to count tokens and their limits.

## Known issues

- The API supports only a number of select languages. Submitting prompts in unsupported languages can produce unexpected or even blocked responses. See [available languages](https://ai.google.dev/gemini-api/docs/models#supported-languages) for updates.

## File a bug

Join the discussion on the
[Google AI developer forum](https://discuss.ai.google.dev)
if you have questions.
# Gemini API Troubleshooting Guide

This file is a project-ready retrieval sheet for common Gemini API and SDK issues, with practical fixes and debugging steps. It is based on the official Gemini troubleshooting guide. [page:2]

## How to use this guide

First identify whether the issue comes from the API backend, the client SDK, model settings, safety filtering, key management, or a request size/rate problem. Then use the matching section below to narrow the cause and fix it systematically. [page:2]

## Quick triage workflow

1. Check your API key setup first.
2. Confirm the model name and API version are valid.
3. Review request shape, token size, and parameter ranges.
4. Check whether the issue is due to rate limits, safety filters, or a temporary service incident. [page:2]

## Common issues and fixes

### 1. Malformed request body
**Symptoms:** HTTP 400 `INVALID_ARGUMENT`.  
**Likely cause:** Missing fields, typos, or an incorrect request format.  
**Fix steps:**
- Compare the request against the API reference.
- Verify required fields and nesting.
- Make sure the endpoint version matches the feature set you are using. [page:2]

### 2. Using newer features on older API versions
**Symptoms:** A request fails even though the syntax looks correct.  
**Likely cause:** The endpoint version does not support the feature.  
**Fix steps:**
- Check whether the feature requires `/v1beta`.
- Upgrade the endpoint if needed.
- Keep request examples aligned with the selected API version. [page:2]

### 3. Free tier not available
**Symptoms:** HTTP 400 `FAILED_PRECONDITION`.  
**Likely cause:** Free tier is not available in your country or billing is not enabled.  
**Fix steps:**
- Enable billing in Google AI Studio.
- Use a paid plan if the free tier is unavailable in your region. [page:2]

### 4. Permission denied
**Symptoms:** HTTP 403 `PERMISSION_DENIED`.  
**Likely cause:** Wrong API key, missing permissions, or improper access to a tuned model.  
**Fix steps:**
- Recheck the API key you are sending.
- Confirm the key has access to the needed project/model.
- Use proper authentication flow for tuned models. [page:2]

### 5. Resource not found
**Symptoms:** HTTP 404 `NOT_FOUND`.  
**Likely cause:** Missing referenced media file or invalid resource path.  
**Fix steps:**
- Validate every referenced image, audio, or video file.
- Confirm the parameters are valid for the API version.
- Retry with a minimal reproducible request. [page:2]

### 6. Rate limits exceeded
**Symptoms:** HTTP 429 `RESOURCE_EXHAUSTED`.  
**Likely cause:** RPM, TPM, RPD, or spending limits have been exceeded.  
**Fix steps:**
- Reduce request rate.
- Reduce prompt size and token usage.
- Retry after a short delay.
- Request a higher limit if your workload justifies it. [page:2]

### 7. Request cancelled
**Symptoms:** HTTP 499 `CANCELLED`.  
**Likely cause:** The client closed the connection too early.  
**Fix steps:**
- Check client-side timeout settings.
- Ensure network middleware is not aborting the request.
- Keep the connection open until the response is complete. [page:2]

### 8. Internal server error
**Symptoms:** HTTP 500 `INTERNAL`.  
**Likely cause:** A Google-side issue or too much context in the prompt.  
**Fix steps:**
- Check Gemini status for incidents.
- Reduce input context length.
- Try a different model temporarily.
- Retry later if the problem persists. [page:2]

### 9. Service unavailable
**Symptoms:** HTTP 503 `UNAVAILABLE`.  
**Likely cause:** Temporary overload or outage.  
**Fix steps:**
- Retry after a short wait.
- Try another model if available.
- Check status for service disruption. [page:2]

### 10. Deadline exceeded
**Symptoms:** HTTP 504 `DEADLINE_EXCEEDED`.  
**Likely cause:** The prompt or context is too large to finish in time.  
**Fix steps:**
- Increase client timeout.
- Shorten the prompt.
- Split the task into smaller requests. [page:2]

### 11. Wrong API key setup
**Symptoms:** Calls fail early or behave like authentication is missing.  
**Likely cause:** API key is not configured correctly.  
**Fix steps:**
- Revisit the API key setup guide.
- Make sure the key is loaded in the right environment.
- Avoid hardcoding secrets in committed code. [page:2]

### 12. Model parameter out of range
**Symptoms:** Request is rejected or behaves unexpectedly.  
**Likely cause:** Candidate count, temperature, topP, or token values are invalid.  
**Fix steps:**
- Keep candidate count between 1 and 8.
- Keep temperature between 0.0 and 1.0.
- Keep topP between 0.0 and 1.0.
- Set max output tokens according to the model’s documented limit. [page:2]

### 13. Wrong model selected
**Symptoms:** The API call works for some tasks but not others.  
**Likely cause:** The model you are using does not support the needed feature.  
**Fix steps:**
- Check the supported models list.
- Match the model to the task.
- Switch to a model that explicitly supports the feature. [page:2]

### 14. High latency on 2.5 models
**Symptoms:** Responses feel slower or consume more tokens than expected.  
**Likely cause:** Thinking is enabled by default on Gemini 2.5 Flash and Pro.  
**Fix steps:**
- Disable thinking if speed and cost matter more than reasoning quality.
- Adjust the thinking configuration in your client. [page:2]

### 15. High token usage
**Symptoms:** Output cost is higher than expected.  
**Likely cause:** Thinking mode or long context.  
**Fix steps:**
- Reduce context size.
- Shorten prompts.
- Reconsider whether thinking is needed for the request. [page:2]

### 16. Safety block
**Symptoms:** Prompt is blocked due to safety settings.  
**Likely cause:** The content triggered configured safety filters.  
**Fix steps:**
- Review the prompt and safety thresholds.
- Adjust safety settings only if appropriate for your application.
- Remove risky phrasing or disallowed content. [page:2]

### 17. `BlockedReason.OTHER`
**Symptoms:** The response is blocked for a reason not clearly labeled.  
**Likely cause:** Terms-of-service or unsupported request pattern.  
**Fix steps:**
- Simplify the request.
- Remove ambiguous or policy-sensitive content.
- Recheck whether the use case is supported. [page:2]

### 18. Recitation stop
**Symptoms:** Generation halts with RECITATION.  
**Likely cause:** The output resembles memorized data too closely.  
**Fix steps:**
- Make the prompt more unique.
- Increase temperature if appropriate.
- Avoid requesting copyrighted or overly familiar text patterns. [page:2]

### 19. Repeated hyphens in tables
**Symptoms:** Markdown tables show awkward repeated separators or formatting noise.  
**Likely cause:** The model is trying to visually align table content.  
**Fix steps:**
- Instruct the model not to pad table cells.
- Use concise columns and simple table formatting.
- Keep separator lines clean and standard. [page:2]

### 20. Repeated tokens in structured output
**Symptoms:** Output loops or duplicates structured fields.  
**Likely cause:** Model is struggling with format constraints.  
**Fix steps:**
- Make all required fields explicit.
- Avoid over-constraining field order.
- Use a simpler response schema if needed. [page:2]

### 21. Repetitive newlines
**Symptoms:** Output contains excessive blank lines.  
**Likely cause:** Escape-sequence or formatting issues in the prompt.  
**Fix steps:**
- Remove problematic escape sequences.
- Use UTF-8 text instead of Unicode escape clutter.
- Make allowed escape patterns explicit. [page:2]

### 22. Repetitive tool calling
**Symptoms:** The model keeps asking for the same tool operation.  
**Likely cause:** The system lost state or is trying an unavailable endpoint repeatedly.  
**Fix steps:**
- Keep the workflow state simple.
- Reduce ambiguous instructions.
- Reframe the task into a single clear step. [page:2]

### 23. Repetitive text outside structured output
**Symptoms:** The assistant repeats itself or loops.  
**Likely cause:** The request may be ambiguous or hard to satisfy.  
**Fix steps:**
- Ask for a simpler output.
- Add a “do not repeat” instruction.
- Lower the complexity of the generation task. [page:2]

### 24. Blocked API key
**Symptoms:** API key returns a leak warning.  
**Likely cause:** Google detected the key as publicly exposed.  
**Fix steps:**
- Generate a new API key in Google AI Studio.
- Replace the leaked key immediately.
- Review how the key was stored or shared. [page:2]

### 25. Unexpected charges after key exposure
**Symptoms:** Billing looks wrong after a leaked key incident.  
**Likely cause:** Unauthorized usage may have occurred.  
**Fix steps:**
- File a billing support case.
- Review logs and usage patterns.
- Rotate secrets and tighten access controls. [page:2]

### 26. Unsupported language behavior
**Symptoms:** Prompts in some languages produce blocked or odd responses.  
**Likely cause:** The API supports only selected languages.  
**Fix steps:**
- Check the supported language list.
- Switch to a supported language if possible.
- Validate multilingual prompts carefully. [page:2]

### 27. Unexpected formatting in code or tables
**Symptoms:** Generated code or tables contain inconsistent formatting.  
**Likely cause:** Prompt instructions are too broad or conflict with formatting needs.  
**Fix steps:**
- Add explicit formatting rules.
- Use cleaner examples.
- Reduce ambiguity in the desired structure. [page:2]

### 28. Request works in one SDK but not another
**Symptoms:** Python works but JS or Go behaves differently, or vice versa.  
**Likely cause:** SDK-specific configuration or version mismatch.  
**Fix steps:**
- Check the matching SDK docs and versions.
- Confirm environment variables and auth setup in each runtime.
- Reproduce with the simplest request first. [page:2]

### 29. Wrong timeout behavior
**Symptoms:** Requests fail too early.  
**Likely cause:** Client timeout is shorter than the model needs.  
**Fix steps:**
- Increase timeout in the client.
- Reduce request size.
- Retry with a smaller prompt. [page:2]

### 30. Need a general debugging path
**Symptoms:** The issue is unclear.  
**Likely cause:** Most Gemini problems come from auth, request format, limits, model choice, or service status.  
**Fix steps:**
- Verify API key.
- Verify model and version.
- Minimize prompt size.
- Check rate limits.
- Test again after a short delay. [page:2]

## Debugging checklist

Use this checklist before escalating:
- Confirm API key setup.
- Confirm the correct model and API version.
- Confirm request parameters are in range.
- Confirm prompt size is reasonable.
- Confirm the issue is not a transient service incident.
- Confirm safety rules are not blocking the request. [page:2]

## Best practices

Keep prompts concise, validate parameters before sending, and design retry logic for 429, 500, 503, and 504 responses. When building apps, log the request shape and response code so failures are easy to reproduce. [page:2]