# Architecture

Qualivanta is a Python/Appium test framework organized around a Page Object Model. This document describes the implemented responsibilities and remaining boundaries.

| Area | Responsibility |
|---|---|
| `config/` | Resolve repository-relative paths, read local/CI environment overrides, validate settings, and construct the capabilities required for Android/Appium sessions. |
| `tests/conftest.py` | Own the per-test driver lifecycle and best-effort failure evidence collection without masking the original failure. |
| `pages/` | Encapsulate screen locators and user actions for login, catalog, product, cart, and checkout flows. |
| `tests/` | Express readable scenarios grouped by smoke, functional, negative, and regression intent. |
| `utilities/` | Provide explicit waits, screenshots, logging, and read-only Android/Java/SDK/Appium diagnostics without hiding failures. |
| `testdata/` | Hold non-secret, reusable login and checkout data in JSON. |
| `scripts/` | Provide opt-in standard-library APK validation/download and generic UI inspection helpers. |
| `docs/` | Preserve architecture, setup, test planning, case inventory, inspection notes, and defect guidance. |
| `reports/` and `artifacts/` | Receive generated HTML/XML reports, screenshots, page-source XML, bounded Logcat excerpts, and CI evidence. |
| `.github/workflows/` | Provision an API 35 Android emulator, start Appium, run pytest, and upload reports/artifacts. |

The execution flow is: pytest selects a scenario, fixtures prepare an isolated Appium session, a test drives page objects, utilities capture evidence on failure, and reporting/CI publishes the result. Selectors and supported behavior are established by inspecting the official demo APK before implementation.

## Design boundaries

- Keep test intent in tests and interaction details in page objects.
- Prefer explicit waits over arbitrary sleeps.
- Keep credentials and machine-specific values out of source control.
- Preserve failure evidence while allowing the original failure to remain visible.
- Treat unsupported demo-app behavior as a documented limitation or replace it with a verified alternative; do not invent selectors or functionality.
