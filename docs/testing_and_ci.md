# Testing and CI guide

Qualivanta uses pytest with Appium-Python-Client, Selenium, and UiAutomator2. Tests use a Page Object Model and a per-test Appium fixture. The local emulator target is API 37; GitHub Actions uses an API 35 emulator with Java 27. CI API 35 is the Android 15 platform configuration; it is distinct from the local API 37 emulator.

## Local commands

From the repository root, with the emulator booted and Appium running:

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m pytest -q -m smoke
.venv\Scripts\python.exe -m pytest -q tests/test_catalog.py tests/test_cart.py tests/test_checkout.py
.venv\Scripts\python.exe -m pytest -q --html=reports/pytest.html --self-contained-html --junitxml=reports/junit.xml
```

Reports are written to `reports/pytest.html` and `reports/junit.xml`. Runtime failure evidence is written to `artifacts/` and may include a screenshot, page-source XML, a bounded Logcat excerpt, and test error context. Evidence collection is best-effort and does not replace the original failure.

## APK and environment

The application under test is Sauce Labs My Demo App Android release 2.3.0. The expected local APK is `demo_app/mda-2.3.0-27.apk`; `mda-androidTest-2.3.0-27.apk` is an auxiliary instrumentation package and is not used by Appium. Validate or retrieve the exact official release asset with:

```powershell
.venv\Scripts\python.exe scripts/download_demo_app.py
```

Local settings are documented in [environment_setup.md](environment_setup.md). CI overrides `APP_PATH`, `ANDROID_UDID=emulator-5554`, `APPIUM_PLATFORM_VERSION=35`, and `APPIUM_SERVER_URL` through the workflow environment.

## GitHub Actions

`.github/workflows/android-tests.yml` runs on pushes, pull requests, and manual dispatch. It installs the pinned Python dependencies, Java 27, Node.js 24.19.0, Appium 3.8.0, and UiAutomator2 8.7.0; downloads/validates the APK; boots an API 35 emulator; waits for Android and Appium readiness; runs the full suite sequentially; and uploads reports and runtime artifacts even when tests fail.

The hosted workflow has completed successfully with **12 passed, 0 failures, 0 errors, and 0 skipped**. The test phase took **266.63 seconds**, and the complete workflow took **6m46s**. GitHub Actions retains the generated reports and runtime artifacts for each run.

## Coverage status and limitations

The repository contains 50 documented scenarios, approximately 27 automation candidates, and 12 implemented automated tests covering smoke, catalog/product details, sorting, cart, and checkout. The remaining documented cases are manual, diagnostic, unsupported, or further-evaluation candidates until separately verified. CI requires GitHub-hosted Android emulator support, network access to the official release metadata, and sufficient runner time for Appium startup and the current suite.
