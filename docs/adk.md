# Google ADK Troubleshooting Guide

This document is a detailed troubleshooting retrieval file for Google Agent Development Kit (ADK). It focuses on installation, environment setup, command issues, runtime failures, tool integration, context problems, and deployment debugging. It is based on the official ADK documentation and common community-reported failure patterns. [page:4][page:5]

## What ADK is

Google ADK is an open-source agent development framework for building, debugging, evaluating, and deploying AI agents in Python, TypeScript, Go, Java, and Kotlin. For Python, the official quickstart requires Python 3.10 or later, `pip`, and the `google-adk` package. [page:4][page:5]

## How to use this file

Use this guide by identifying the stage where the failure occurs: installation, virtual environment, command line, agent creation, tool use, API key setup, runtime errors, evaluation, or deployment. Then follow the matching checklist and fix steps below. [page:4][page:5]

## Quick triage flow

1. Confirm the Python version is supported.
2. Confirm the virtual environment is activated.
3. Confirm `google-adk` is installed in the active environment.
4. Confirm the `adk` command is on the PATH.
5. Confirm the Gemini API key or other model auth is configured correctly.
6. Confirm the agent project structure is valid.
7. Confirm the issue is not caused by a tool, model, or deployment configuration problem. [page:5]

## Common issues and fixes

### 1. Python version too old
**Symptoms:** ADK installation fails, commands do not work, or `adk` features are missing.  
**Likely cause:** The environment is using an unsupported Python version.  
**Fix steps:**
- Check your version with `python --version`.
- Use Python 3.10 or later for the official Python quickstart.
- Create a fresh environment after upgrading Python. [page:5]

### 2. `pip` not installed
**Symptoms:** `pip` is missing or `pip install google-adk` fails.  
**Likely cause:** Python was installed without package tooling or PATH is wrong.  
**Fix steps:**
- Verify `pip --version`.
- Install or repair `pip`.
- Reopen the terminal after installation so PATH updates take effect. [page:5]

### 3. Virtual environment not activated
**Symptoms:** ADK seems installed but commands fail in the current terminal.  
**Likely cause:** `google-adk` was installed in a different interpreter or venv.  
**Fix steps:**
- Create a venv with `python3 -m venv .venv`.
- Activate it before installing or running ADK.
- On Windows use the correct activation script; on macOS/Linux use `source .venv/bin/activate`. [page:5]

### 4. `adk` command not found
**Symptoms:** Terminal says `command not found: adk`.  
**Likely cause:** The ADK executable is not on PATH or the wrong environment is active.  
**Fix steps:**
- Run `python -m pip list` to confirm `google-adk` is installed.
- Find the executable path with `which adk` or the equivalent on your OS.
- Add the ADK binary directory to PATH if needed.
- Reopen the terminal and try again. [page:5]

### 5. Installed package in wrong environment
**Symptoms:** `google-adk` appears installed, but `adk run` still fails.  
**Likely cause:** The package was installed globally while the terminal uses a venv, or vice versa.  
**Fix steps:**
- Activate the intended venv first.
- Reinstall `google-adk` inside that environment.
- Confirm `python -m pip show google-adk` points to the same interpreter. [page:5]

### 6. `adk` creates the wrong project structure
**Symptoms:** The generated project folder is incomplete or hard to run.  
**Likely cause:** Project was not created from the correct directory or the scaffolding was interrupted.  
**Fix steps:**
- Run `adk create my_agent` from a clean working directory.
- Confirm the generated folder contains `agent.py`, `.env`, and `__init__.py`.
- Delete broken scaffolds and recreate if necessary. [page:5]

### 7. `adk create` fails
**Symptoms:** Project creation command exits with an error.  
**Likely cause:** Environment, PATH, permissions, or package installation issues.  
**Fix steps:**
- Confirm Python, pip, and venv are working.
- Ensure the active environment contains `google-adk`.
- Retry the command from a normal user shell rather than a restricted session. [page:5]

### 8. `adk run` cannot find the agent
**Symptoms:** `adk run my_agent` fails even though the folder exists.  
**Likely cause:** You ran the command from the wrong directory or the project structure is wrong.  
**Fix steps:**
- Run the command from the parent directory that contains the agent folder.
- Verify the folder name matches the command exactly.
- Ensure `agent.py` exists in the agent package. [page:5]

### 9. `adk web` shows no agent
**Symptoms:** Web UI opens but the agent does not appear.  
**Likely cause:** The command was launched from the wrong directory or the project is not structured correctly.  
**Fix steps:**
- Start `adk web` from the parent directory containing the agent project.
- Verify the root agent is defined in `agent.py`.
- Refresh the UI after correcting the path. [page:5]

### 10. ADK Web should not be used in production
**Symptoms:** You want to deploy the web UI publicly.  
**Likely cause:** ADK Web is a development/debugging interface only.  
**Fix steps:**
- Use ADK Web locally for development.
- Do not treat it as a production deployment target.
- Use the proper deployment path for production agents. [page:5]

### 11. `.env` not loading
**Symptoms:** The agent cannot read `GOOGLE_API_KEY` or other environment variables.  
**Likely cause:** The `.env` file is missing, misnamed, or in the wrong directory.  
**Fix steps:**
- Put `.env` in the agent project root.
- Ensure the variable name is exactly correct.
- Restart the shell or process after changing environment values. [page:5]

### 12. API key missing
**Symptoms:** The agent fails immediately when trying to call the Gemini model.  
**Likely cause:** `GOOGLE_API_KEY` is not set.  
**Fix steps:**
- Create a Gemini API key in Google AI Studio.
- Save it as `GOOGLE_API_KEY` in the project environment.
- Avoid committing secrets to source control. [page:5]

### 13. Wrong API key
**Symptoms:** Authentication errors even though a key exists.  
**Likely cause:** The wrong project key or stale key is being used.  
**Fix steps:**
- Recheck the environment variable value.
- Replace old keys with a new valid key.
- Confirm the key belongs to the intended Google project. [page:5]

### 14. Agent file missing `root_agent`
**Symptoms:** ADK cannot load the agent.  
**Likely cause:** The required root agent definition is absent or named incorrectly.  
**Fix steps:**
- Define `root_agent` in `agent.py`.
- Match the structure shown in the quickstart.
- Keep the root agent definition simple and explicit. [page:5]

### 15. Wrong import path for Agent
**Symptoms:** Import errors occur in `agent.py`.  
**Likely cause:** The code is using an outdated or incorrect import path.  
**Fix steps:**
- Compare your imports to the current quickstart.
- Update the ADK package if the example is outdated.
- Keep your code aligned with the installed ADK version. [page:4][page:5]

### 16. Model name is invalid
**Symptoms:** The agent fails when trying to load a model.  
**Likely cause:** Incorrect model name or unsupported model string.  
**Fix steps:**
- Confirm the model name exists in ADK’s supported model setup.
- Start with the official example model string.
- Test with a known working model before switching to a custom one. [page:4][page:5]

### 17. Agent does not answer as expected
**Symptoms:** The agent runs but gives poor or irrelevant responses.  
**Likely cause:** Weak instructions, missing tool wiring, or poor model selection.  
**Fix steps:**
- Improve the agent instruction.
- Confirm the right tool is passed to `tools=[...]`.
- Test with a more specific prompt and narrower task. [page:4]

### 18. Tool never gets called
**Symptoms:** The agent ignores a tool that should be used.  
**Likely cause:** The instruction does not clearly tell the model when to use the tool.  
**Fix steps:**
- Make the instruction explicit about tool usage.
- Verify the tool is included in the agent constructor.
- Test the tool independently before attaching it to the agent. [page:5]

### 19. Tool schema mismatch
**Symptoms:** Tool execution fails or arguments are wrong.  
**Likely cause:** Function signature and expected tool schema do not match.  
**Fix steps:**
- Simplify the tool function signature.
- Keep parameter names clear and consistent.
- Validate tool input manually before testing the agent. [page:4]

### 20. Tool failure crashes workflow
**Symptoms:** One tool error breaks the entire agent run.  
**Likely cause:** Unhandled tool exceptions are propagating through the workflow.  
**Fix steps:**
- Add try/except handling inside the tool.
- Return structured error objects rather than raw exceptions.
- Test error states intentionally before release. [web:19]

### 21. Multi-agent workflow gets stuck
**Symptoms:** Orchestration does not complete or loops endlessly.  
**Likely cause:** Agent handoff logic, context, or graph design is wrong.  
**Fix steps:**
- Simplify the workflow first.
- Confirm each agent has one clear responsibility.
- Inspect handoff and graph transitions carefully. [page:4]

### 22. Context grows too large
**Symptoms:** Slow responses, token waste, or degraded reasoning.  
**Likely cause:** Too much conversation or tool output is being kept.  
**Fix steps:**
- Reduce unnecessary context.
- Keep only relevant tool output.
- Use structured summaries for long-running sessions. [page:4]

### 23. Context drops important information
**Symptoms:** The agent forgets earlier steps or loses state.  
**Likely cause:** Context management is too aggressive or state is not stored well.  
**Fix steps:**
- Preserve key state in artifacts or explicit memory structures.
- Verify important events are retained.
- Avoid over-trimming useful context. [page:4]

### 24. Evaluation results are poor
**Symptoms:** The agent works inconsistently in tests.  
**Likely cause:** Weak test design or inadequate golden data.  
**Fix steps:**
- Create clear evaluation datasets.
- Test the most important edge cases.
- Use ADK evaluation workflows instead of ad hoc checks. [page:4]

### 25. Deployment fails to Google Cloud
**Symptoms:** The agent works locally but not in cloud deployment.  
**Likely cause:** Container, runtime, auth, or infrastructure mismatch.  
**Fix steps:**
- Recheck deployment prerequisites.
- Verify local and cloud environment parity.
- Review logs from the deployment target carefully. [page:4]

### 26. Local and cloud behavior differ
**Symptoms:** The same agent behaves differently after deployment.  
**Likely cause:** Environment variables, auth, or runtime differences.  
**Fix steps:**
- Compare local and cloud env configs.
- Check model authentication in the cloud target.
- Reproduce the issue with the smallest possible input. [page:4]

### 27. Missing logs make debugging hard
**Symptoms:** Errors are vague and hard to trace.  
**Likely cause:** Logging is not configured or not being inspected.  
**Fix steps:**
- Add structured logs around tool calls and agent steps.
- Capture request/response metadata where safe.
- Review cloud and local logs side by side. [page:4]

### 28. Agent works in CLI but not web UI
**Symptoms:** `adk run` works, but `adk web` does not.  
**Likely cause:** Directory launch context or UI-specific startup issue.  
**Fix steps:**
- Start both commands from the correct parent directory.
- Recheck the project structure.
- Compare environment variables used by both commands. [page:5]

### 29. Package version mismatch
**Symptoms:** The agent breaks after upgrading or mixing package versions.  
**Likely cause:** ADK or dependency versions are incompatible.  
**Fix steps:**
- Pin the working version first.
- Upgrade dependencies one at a time.
- Recreate the environment if version drift becomes messy. [web:13][web:16]

### 30. `google-cloud-aiplatform` conflict
**Symptoms:** Dependency resolution fails during install or upgrade.  
**Likely cause:** Version mismatch between ADK and Vertex AI-related packages.  
**Fix steps:**
- Check the exact package requirements before upgrading.
- Align `google-cloud-aiplatform` with the ADK release you are using.
- Remove conflicting older dependencies if necessary. [web:13]

### 31. Older Python installs ADK incorrectly
**Symptoms:** ADK installs but functionality is missing.  
**Likely cause:** Very old Python versions may install outdated package behavior.  
**Fix steps:**
- Upgrade Python to a modern supported release.
- Recreate the virtual environment.
- Reinstall ADK from scratch. [web:16]

### 32. Windows terminal permission errors
**Symptoms:** Commands fail only on Windows.  
**Likely cause:** Shell permissions or activation issues.  
**Fix steps:**
- Run the terminal with the right privileges if needed.
- Activate the venv correctly.
- Confirm the interpreter path in VS Code matches the venv. [web:18]

### 33. VS Code uses the wrong interpreter
**Symptoms:** Code runs in one terminal but not in the editor.  
**Likely cause:** VS Code selected a different Python interpreter.  
**Fix steps:**
- Choose the interpreter from the `.venv`.
- Reload the window.
- Recheck launch configuration and terminal shell. [web:18]

### 34. Agent installation seems successful but commands fail after reopening terminal
**Symptoms:** ADK works in one shell session only.  
**Likely cause:** Environment activation is not persistent.  
**Fix steps:**
- Re-activate the virtual environment in each new terminal.
- Confirm PATH is set correctly.
- Save the setup steps in your project README. [web:16]

### 35. Search or retrieval tool not working
**Symptoms:** Agent cannot use a tool even though it is defined.  
**Likely cause:** Missing setup, wrong permission, or tool integration bug.  
**Fix steps:**
- Test the tool as a standalone function first.
- Confirm the agent passes it through the constructor.
- Check logs and tool input/output formatting. [page:4][web:19]

### 36. Output formatting is unstable
**Symptoms:** The agent produces inconsistent structured output.  
**Likely cause:** Prompt and schema constraints are not clear enough.  
**Fix steps:**
- Add explicit output format instructions.
- Keep the schema simple.
- Validate the output in code before trusting it downstream. [page:4]

### 37. Rate or quota issues with model calls
**Symptoms:** Requests start failing after repeated usage.  
**Likely cause:** Model or API quota limits.  
**Fix steps:**
- Throttle requests.
- Add retries with backoff.
- Reduce unnecessary calls inside loops. [page:4]

### 38. Agent behaves unpredictably with long tasks
**Symptoms:** Multi-step tasks are inconsistent.  
**Likely cause:** State, memory, or tool control is not managed well.  
**Fix steps:**
- Break the workflow into smaller steps.
- Use explicit intermediate artifacts.
- Keep each agent responsibility narrow. [page:4]

### 39. Agent cannot be debugged easily
**Symptoms:** You cannot tell where the failure is happening.  
**Likely cause:** Too much abstraction or not enough observability.  
**Fix steps:**
- Test agent, tool, and model independently.
- Add logs at each boundary.
- Reproduce on a minimal example. [page:4]

### 40. General “it just doesn’t work” case
**Symptoms:** No single error message explains the issue.  
**Likely cause:** One of the common layers is broken: Python, venv, PATH, import, key, tool, model, or deployment.  
**Fix steps:**
- Check Python version.
- Check venv activation.
- Check `adk` path.
- Check `.env` and API key.
- Check agent structure.
- Check tool definitions.
- Check logs. [page:4][page:5]

## Practical checklist

Use this checklist before escalating an ADK issue:
- Python 3.10+ is installed. [page:5]
- The virtual environment is active. [page:5]
- `google-adk` is installed in that environment. [page:5]
- `adk create`, `adk run`, and `adk web` are launched from the correct directory. [page:5]
- `GOOGLE_API_KEY` is set in `.env`. [page:5]
- `root_agent` is defined in `agent.py`. [page:5]
- Tool functions are tested independently. [page:4]
- The model name is valid for the current setup. [page:4]
- Logs are enabled and reviewed during failures. [page:4]
- Version conflicts are checked after upgrades. [web:13][web:16]

## Best practices

Keep your agent code small at first, add one tool at a time, and verify behavior after each change. Use ADK Web for development only, pin package versions when things are stable, and maintain a minimal reproducible example for debugging future issues. [page:4][page:5][web:13]