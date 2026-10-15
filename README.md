# Qualivanta

Qualivanta is a professional Android mobile QA automation framework for a Graduate Trainee — Automation Testing portfolio. It is being designed to demonstrate maintainable test automation, clear evidence, and disciplined test documentation against Sauce Labs' My Demo App for Android.

## Project status

**Implemented baseline.** The project contains a working local Appium vertical slice with 12 automated tests covering smoke, catalog/product details, sorting, cart, and checkout. GitHub Actions CI and failure-reporting support are configured but require a hosted workflow run for CI evidence.

## Technology stack

- Python 3.14.4
- Appium 3.8.0 with UiAutomator2 driver 8.7.0
- Appium-Python-Client 6.0.7
- Selenium 4.51.0
- pytest 9.1.1 and pytest-html 4.2.0
- Java 27 and Android Studio Emulator API 37 for local development
- GitHub Actions with Android API 35 and Java 27 planned for CI
- Sauce Labs My Demo App for Android, official release 2.3.0

Direct Python dependencies are pinned in [requirements.txt](requirements.txt). A generated lock file is intentionally deferred until the environment is installed and verified.

## Planned architecture

The framework will use a Page Object Model. Configuration and capabilities will centralize environment settings; fixtures will manage driver lifecycle and state isolation; page objects will represent app screens; tests will express scenarios; utilities will provide waits, screenshots, logging, and Android diagnostics; and reports/artifacts will preserve execution evidence. See [docs/architecture.md](docs/architecture.md).

The inventory contains 50 documented cases, approximately 27 planned automation candidates, and 12 implemented automated tests. The remaining cases are manual, diagnostic, unsupported, or further-evaluation candidates. See [docs/test_cases.md](docs/test_cases.md).

## Planned project layout

```text
config/       Settings and Appium capabilities
pages/        Page Object Model classes
tests/        pytest scenarios and fixtures
testdata/     Externalized test data
utilities/    Waits, evidence, logging, diagnostics
scripts/      Local support scripts
docs/         Architecture, setup, plan, cases, and defect guidance
apps/         Local APK downloads (ignored by Git)
reports/      Generated HTML reports (ignored by Git)
artifacts/    Runtime screenshots, logs, and CI evidence (ignored by Git)
```

## Local Windows setup

The beginner-friendly setup notes are in [docs/environment_setup.md](docs/environment_setup.md). The pinned dependencies, APK validation helper, driver configuration, page objects, fixtures, and automated tests are implemented; follow the guide to run them locally.

The agreed local settings are:

- Java home: `E:\softwares\Java`
- Android SDK: `C:\Users\HP\AppData\Local\Android\Sdk`
- AVD: `Qualivanta_API_37`
- Appium server: `http://127.0.0.1:4723`

The expected PowerShell flow is:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Boot the Qualivanta_API_37 emulator and start Appium first.
.venv\Scripts\python.exe -m pytest -q
```

See [docs/testing_and_ci.md](docs/testing_and_ci.md) for smoke, feature-group, and HTML/JUnit report commands.

## Evidence and CI plan

The framework captures failure screenshots, Appium page-source XML, bounded Logcat excerpts, and test error context under `artifacts/`. HTML and JUnit results are written under `reports/`. GitHub Actions boots an Android API 35 emulator under Java 27, runs the suite sequentially, and uploads reports and artifacts even when tests fail. The workflow has not been executed in GitHub Actions from this workspace.

## Further reading

- [Architecture](docs/architecture.md)
- [Environment setup](docs/environment_setup.md)
- [Test plan](docs/test_plan.md)
- [50-case test inventory](docs/test_cases.md)
- [Defect template](docs/defect_template.md)
