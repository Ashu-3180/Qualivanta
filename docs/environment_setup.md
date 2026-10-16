# Windows environment setup

This is a beginner-friendly guide for local execution. It does not change machine or user environment variables.

## Agreed local tools and locations

- Python: 3.14.4
- Java home: `E:\softwares\Java`
- Android SDK: `C:\Users\HP\AppData\Local\Android\Sdk`
- Android Studio Emulator AVD: `Qualivanta_API_37`
- Appium server URL: `http://127.0.0.1:4723`
- Appium: 3.8.0; UiAutomator2 driver: 8.7.0
- Appium-Python-Client: 6.0.7
- Selenium: 4.51.0
- pytest: 9.1.1; pytest-html: 4.2.0

Use the installed Java and SDK locations above. Do not modify machine or user environment variables as part of this project setup.

## PowerShell sequence

From the repository root:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The existing main application APK is at `demo_app/mda-2.3.0-27.apk`. The `demo_app/mda-androidTest-2.3.0-27.apk` file is an auxiliary instrumentation-test package and must never be supplied as the Appium application under test.

## APK validation

The validation/download helper reuses a valid local APK and prints its SHA-256 digest:

```powershell
python scripts/download_demo_app.py
```

If the main APK is missing, the helper retrieves only the exact `mda-2.3.0-27.apk` asset from the official Sauce Labs GitHub release tagged `2.3.0`. It validates ZIP integrity and `AndroidManifest.xml` before moving the download into place. An existing invalid APK is left untouched and reported as an error.

## Before execution

1. Start Android Studio's `Qualivanta_API_37` emulator and wait until Android has finished booting.
2. Start Appium and confirm it is listening at `http://127.0.0.1:4723`.
3. Use the read-only diagnostic functions in `utilities/android_diagnostics.py` to check ADB, boot completion, Java, SDK paths, device metadata, and Appium readiness.
4. Capture a generic screen and page-source snapshot only when explicitly inspecting the app:

   ```powershell
   python scripts/capture_ui_snapshot.py --name initial_screen
   ```

   This starts and closes one Appium session, then writes PNG/XML evidence under `docs/app_inspection/`. It does not assume that the initial screen is a login screen.
5. Confirm the capability configuration points to the booted emulator and verified APK.
6. Run the implemented suite with `.venv\Scripts\python.exe -m pytest -q`.

For report commands, feature-group commands, failure artifacts, and CI details, see [testing_and_ci.md](testing_and_ci.md).

## Troubleshooting

- **Missing APK:** run `python scripts/download_demo_app.py`; check that `APP_PATH` points to the main APK, not the instrumentation-test APK.
- **Offline device:** start `Qualivanta_API_37`, wait for Android to finish booting, and verify `emulator-5554` is listed by `adb devices` with state `device`.
- **Unreachable Appium:** start Appium and verify `http://127.0.0.1:4723/status` is reachable. The snapshot utility reports a clear error without starting or stopping Appium.
- **CI/API differences:** set `ANDROID_UDID`, `APPIUM_PLATFORM_VERSION=35`, `APP_PATH`, `ANDROID_HOME`, and `APPIUM_SERVER_URL` in CI; no source-code path change is required.

GitHub Actions uses an Android API 35 emulator with Java 27. In Android terminology, API 35 is the Android 15 platform configuration; the local emulator remains API 37.
