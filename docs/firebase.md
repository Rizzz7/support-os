# Quick Diagnosis

| Symptom | Go To |
|---------|-------|
| Deploy stuck | Issue 1 |
| Repository missing | Issue 2 |
| GitHub auth failed | Issue 3 |
| Build invalid | Issue 7 |
| Cloud Run failure | Issue 8 |
| CDN not caching | Issue 15 |
| Angular build fails | Issue 20 |
| Next.js middleware | Issue 25 |

















# Firebase App Hosting Troubleshooting Guide

This file is a project-ready troubleshooting retrieval sheet for Firebase App Hosting, focused on the most common issues, likely causes, and practical fixes. It is based on Firebase’s official App Hosting troubleshooting documentation and related limitation notes. [web:1]

## How to use this guide

When a deployment, runtime, or console issue happens, first identify where it fails: console setup, GitHub connection, build, deploy, Cloud Run, CDN, or framework-specific behavior. Then jump to the matching issue below and follow the checks in order. [web:1]

## Quick triage workflow

1. Check whether the issue is isolated to one backend or all backends in the project.
2. Verify GitHub repository access, backend configuration, and framework compatibility.
3. Confirm whether the problem is a known limitation of Angular, Next.js, or general App Hosting behavior.
4. If deployment latency is unusually slow in a region, test a different region. [web:1]

## Common issues and fixes

### 1. Deployment is slower than expected
**Symptoms:** Backend creation or updates take longer than expected.  
**Likely cause:** Cloud Run infrastructure delays in certain regions, including examples noted by Google.  
**Fix steps:**
- Wait and retry if it is a temporary delay.
- If the delay is persistent, deploy to another supported region.
- Compare rollout timing across regions to isolate a regional issue. [web:1]

### 2. Repository does not appear in Firebase console
**Symptoms:** Your GitHub repo is missing when creating a backend.  
**Likely cause:** App Hosting has not refreshed repository permissions.  
**Fix steps:**
- Click **Refresh list** in the Firebase console.
- Use **Grant access to a new repository in GitHub** if the repo is not visible.
- Open GitHub profile settings, then **Applications**, then **Firebase App Hosting**, and verify repository access. [web:1]

### 3. GitHub access is not working
**Symptoms:** Backend setup fails while connecting GitHub.  
**Likely cause:** GitHub app permissions are incomplete or the wrong org/account is selected.  
**Fix steps:**
- Confirm the correct GitHub org/account is connected.
- Recheck permissions in the Firebase App Hosting GitHub application.
- Remove and reconnect the GitHub integration if access is broken. [web:1]

### 4. Cannot use GitLab or another Git provider
**Symptoms:** You want to deploy from GitLab, Bitbucket, or another provider.  
**Likely cause:** App Hosting currently supports GitHub only.  
**Fix steps:**
- Use GitHub for the deployment pipeline.
- Monitor Firebase roadmap for future provider support. [web:1]

### 5. Cannot change repository for an existing backend
**Symptoms:** You want the same backend to point to a different repo.  
**Likely cause:** Repository changes are not supported directly.  
**Fix steps:**
- Create a new backend in the same project for the new repository.
- Or create a separate project if you need a different GitHub account. [web:1]

### 6. Different GitHub accounts in one project
**Symptoms:** Multiple backends need different GitHub accounts.  
**Likely cause:** All backends in one project share the same GitHub org/account.  
**Fix steps:**
- Keep repositories under the same GitHub org/account inside one project.
- Use separate Firebase projects for separate GitHub accounts. [web:1]

### 7. “Build was not found and is invalid”
**Symptoms:** Firebase console shows this message during backend creation.  
**Likely cause:** Intermittent console-side issue.  
**Fix steps:**
- Retry backend creation.
- Refresh the page and recheck backend status.
- If it keeps happening, test again later because the issue is described as intermittent. [web:1]

### 8. App Hosting errors but Cloud Build looks fine
**Symptoms:** Console shows App Hosting failure, but Cloud Build appears successful.  
**Likely cause:** The failure may actually be in Cloud Run or rollout staging.  
**Fix steps:**
- Inspect the rollout status carefully.
- Treat Cloud Build success as only one part of the pipeline.
- Check Cloud Run logs and deployment phase status next. [web:1]

### 9. Framework other than Next.js or Angular fails
**Symptoms:** Non-standard framework builds fail or behave unpredictably.  
**Likely cause:** App Hosting officially optimizes support for Next.js and Angular; other frameworks may rely on community adapters or generic Node.js support.  
**Fix steps:**
- Use a supported framework adapter if available.
- Ensure the app has a valid build and start script.
- Do not expect guaranteed success for arbitrary Node.js frameworks. [web:1]

### 10. Generic Node.js app build fails
**Symptoms:** App Hosting cannot complete build or start.  
**Likely cause:** Your Node app may not match App Hosting expectations.  
**Fix steps:**
- Verify build and start scripts in `package.json`.
- Ensure dependencies install cleanly.
- Reduce framework-specific assumptions and test locally first. [web:1]

### 11. App cannot be tested locally
**Symptoms:** You want a pre-deploy test environment.  
**Likely cause:** Local testing is not configured or you are not using the emulator.  
**Fix steps:**
- Use the Firebase Local Emulator Suite.
- Run the App Hosting emulator for local deployment tests.
- Validate environment variables and routing before production deploy. [web:1]

### 12. Custom domain does not display properly in Android WebView
**Symptoms:** Site works in browsers but fails in Android app WebView.  
**Likely cause:** Older custom-domain records created before Q3 2025 may be incompatible.  
**Fix steps:**
- Remove the custom domain from the backend.
- Re-add it from the updated console UI.
- Use the new A, TXT, and ACME challenge CNAME records. [web:1]

### 13. Site headers are difficult to configure
**Symptoms:** You need custom response headers.  
**Likely cause:** Headers are framework-dependent rather than managed centrally.  
**Fix steps:**
- Configure headers in your framework’s normal way.
- For Next.js or Angular, follow framework-specific deployment conventions. [web:1]

### 14. App Hosting region support is unclear
**Symptoms:** You need a region that fits your deployment goals.  
**Likely cause:** Supported regions expand over time.  
**Fix steps:**
- Check the latest App Hosting locations page.
- If one region is slow, test another supported region. [web:1]

### 15. CDN does not cache a response
**Symptoms:** Static or dynamic responses behave like uncached content.  
**Likely cause:** The response `Vary` header includes values not supported in App Hosting cache keys.  
**Fix steps:**
- Review the `Vary` header.
- Keep only supported request headers in cache-key behavior.
- Avoid unsupported `Vary` combinations that prevent caching. [web:1]

### 16. Unexpected cache miss on Next.js
**Symptoms:** Next.js pages or assets are cached poorly.  
**Likely cause:** Middleware and header behavior can reduce cache hit rates.  
**Fix steps:**
- Check whether middleware is involved.
- Minimize unsupported cache variability.
- Expect gradual improvement where Firebase notes caching limitations. [web:1]

### 17. Static files seem slower than expected
**Symptoms:** Static assets load from the backend rather than instantly from edge cache.  
**Likely cause:** Uncached static files are currently served from Cloud Run.  
**Fix steps:**
- Optimize static asset caching patterns.
- Reduce unnecessary cache-busting.
- Track future platform improvements for origin-side serving. [web:1]

### 18. Angular direct navigation to SSR pages fails
**Symptoms:** Directly opening SSR routes in Angular causes errors.  
**Likely cause:** Angular I18n and SSR navigation limitations.  
**Fix steps:**
- Test route entry through standard navigation flows.
- Avoid assuming all direct SSR routes behave identically.
- Verify against current Angular App Hosting compatibility notes. [web:1]

### 19. Angular localization build fails
**Symptoms:** Builds for different locales do not work.  
**Likely cause:** Localization builds are not supported.  
**Fix steps:**
- Avoid multi-locale build expectations in App Hosting.
- Handle locale strategy outside the unsupported deployment path. [web:1]

### 20. Angular builder issue
**Symptoms:** Build fails due to unsupported builder configuration.  
**Likely cause:** Only the Application builder is supported.  
**Fix steps:**
- Switch to the Application builder.
- Remove unsupported builder configurations. [web:1]

### 21. Angular monorepo build fails
**Symptoms:** Projects with more than one application target fail.  
**Likely cause:** Current App Hosting limitations for Angular monorepo tooling.  
**Fix steps:**
- Simplify to a single application target.
- For stronger monorepo support, use Nx. [web:1]

### 22. Angular HTTP 400 on SSR
**Symptoms:** SSR pages return HTTP 400 or host-validation errors.  
**Likely cause:** Proxy trust configuration or dependency mismatch.  
**Fix steps:**
- For Angular v19, v20, and v21, run `npm update @angular/core @angular/ssr`.
- Or set `trustProxyHeaders: true` in server config.
- For Angular v22, build a second time on a new backend if the first build returns 400. [web:1]

### 23. Next.js image optimization is off
**Symptoms:** Images are not optimized automatically.  
**Likely cause:** Built-in Next.js image optimization is disabled by default.  
**Fix steps:**
- Set `images.unoptimized` to `false` when appropriate.
- Or configure a custom Image Loader. [web:1]

### 24. Next.js parallel routing breaks on encoded paths
**Symptoms:** Route matching behaves oddly with percent-encoded URLs.  
**Likely cause:** Cloud Run decodes encoded characters in URL paths.  
**Fix steps:**
- Review route assumptions involving encoded characters.
- Avoid designs that require encoded path preservation for routing logic. [web:1]

### 25. Next.js middleware cache rates are low
**Symptoms:** Pages behind middleware are cached inconsistently.  
**Likely cause:** App Hosting currently limits caching for Next.js middleware apps.  
**Fix steps:**
- Reduce unnecessary middleware complexity.
- Re-evaluate caching assumptions in middleware-heavy routes. [web:1]

### 26. Repository belongs to wrong org/account
**Symptoms:** The repo is visible, but deployment setup still fails.  
**Likely cause:** The backend and repository are under mismatched account assumptions.  
**Fix steps:**
- Confirm the GitHub org/account linked to the project.
- Recreate the backend in the correct project if needed. [web:1]

### 27. Backend creation errors repeat randomly
**Symptoms:** Errors appear inconsistently during backend creation.  
**Likely cause:** Console or infrastructure timing issues.  
**Fix steps:**
- Retry after a short delay.
- Refresh console state and try again.
- Move to another region if regional latency is the suspected cause. [web:1]

### 28. App works in browser but not embedded contexts
**Symptoms:** Browser works, but Android WebView or embedded app view fails.  
**Likely cause:** Domain-record compatibility or WebView-specific behavior.  
**Fix steps:**
- Recreate custom domain records using the newer console flow.
- Test without the old CNAME setup. [web:1]

### 29. App Hosting support expectations are too broad
**Symptoms:** You expect every framework feature to work out of the box.  
**Likely cause:** App Hosting is best supported for Next.js and Angular, with limited guarantees for other stacks.  
**Fix steps:**
- Confirm framework support before deployment.
- Use documented adapters where available.
- Validate the app with local emulation before production. [web:1]

### 30. Need a root-cause checklist
**Symptoms:** You have no idea where the failure is happening.  
**Likely cause:** Many App Hosting issues come from configuration, framework mismatch, or platform limitations.  
**Fix steps:**
- Check repo access.
- Check backend and region.
- Check framework limitations.
- Check Cloud Run and rollout status.
- Check whether the issue is a known limitation or a transient infra problem. [web:1]

## Field checklist

Use this checklist before escalating an issue:
- Confirm the repository is connected to the correct GitHub org/account.
- Verify the framework is supported or adapted correctly.
- Test the app with the App Hosting emulator.
- Check whether the problem matches a listed limitation.
- Try another region if deployment latency is high.
- Review Cloud Run rollout status if App Hosting and Cloud Build disagree. [web:1]

## Best practices

Keep cache headers simple, avoid unsupported `Vary` behavior, and do not assume that all Next.js or Angular features are available immediately on App Hosting. When in doubt, isolate the problem by testing locally, then in a new backend, then in a different region. [web:1]