# Test plan

## Scope and objectives

The scope is the Android My Demo App release 2.3.0: authentication, catalog/product browsing, cart behavior, checkout, navigation, and framework reliability. The objectives are to verify user-critical flows, document negative behavior, preserve evidence, and demonstrate maintainable automation suitable for a Graduate Trainee portfolio.

## Entry criteria

- The APK has been inspected and its supported behavior and selectors are recorded.
- The local emulator or CI emulator is booted and reachable.
- Appium is available at the configured endpoint.
- Dependencies, fixtures, page objects, and test data are implemented and reviewed.

## Exit criteria

- The planned automated candidates have been executed in the target environment.
- Failures have triage notes and retained screenshots/logs where applicable.
- The 50-case inventory has been updated with verified support and final status.
- Reports and CI artifacts are available for the executed run.

## Categories

Authentication; catalog and product details; shopping cart; checkout; navigation; and framework reliability. The full inventory is in [test_cases.md](test_cases.md).

## Risks and limitations

The demo app may not support every proposed scenario, selectors may vary by build, emulator timing can be variable, and CI emulator performance may differ from local API 37. These risks require APK inspection and explicit waits. Unsupported cases must be replaced with verified alternatives while preserving 50 documented cases and approximately 27 meaningful automation candidates.

## Evidence

Planned evidence includes pytest/HTML results, failure screenshots, Logcat diagnostics, and GitHub Actions artifacts. None of these execution outputs are claimed by this scaffold.
