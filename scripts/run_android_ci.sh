#!/usr/bin/env bash

set -euo pipefail

# Always run from the repository root.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p artifacts reports

SERIAL="${ANDROID_UDID:-${ANDROID_SERIAL:-emulator-5554}}"

echo "Using Android device: $SERIAL"
echo "Waiting for the emulator..."

adb -s "$SERIAL" wait-for-device

# Verify that Android has completed booting.
BOOT_STATUS=""

for attempt in $(seq 1 60); do
    BOOT_STATUS="$(
        adb -s "$SERIAL" shell getprop sys.boot_completed 2>/dev/null |
            tr -d '\r' || true
    )"

    if [ "$BOOT_STATUS" = "1" ]; then
        break
    fi

    sleep 2
done

if [ "$BOOT_STATUS" != "1" ]; then
    echo "ERROR: Android did not finish booting."

    adb devices -l > artifacts/adb-devices.txt 2>&1 || true

    adb -s "$SERIAL" logcat -d -t 4000 \
        > artifacts/emulator-logcat.txt 2>&1 || true

    exit 1
fi

echo "Android boot completed successfully."

# Start Appium in the background.
appium \
    --address 127.0.0.1 \
    --port 4723 \
    > artifacts/appium.log 2>&1 &

APPIUM_PID=$!

cleanup() {
    kill "$APPIUM_PID" 2>/dev/null || true
}

trap cleanup EXIT

# Wait for the Appium server to become ready.
APPIUM_READY="false"

for attempt in $(seq 1 60); do
    if curl --fail --silent \
        http://127.0.0.1:4723/status \
        > artifacts/appium-status.json; then

        APPIUM_READY="true"
        break
    fi

    if ! kill -0 "$APPIUM_PID" 2>/dev/null; then
        echo "ERROR: The Appium process exited during startup."
        break
    fi

    sleep 2
done

if [ "$APPIUM_READY" != "true" ]; then
    echo "ERROR: Appium did not become ready."

    cat artifacts/appium.log || true

    exit 1
fi

echo "Appium is ready."
echo "Running the complete Qualivanta test suite..."

# Preserve the pytest exit code while collecting diagnostics on failure.
if python -m pytest -q \
    --html=reports/pytest.html \
    --self-contained-html \
    --junitxml=reports/junit.xml; then

    echo "Qualivanta test suite passed."

else
    TEST_EXIT_CODE=$?

    echo "ERROR: Pytest failed with exit code $TEST_EXIT_CODE."
    echo "Collecting Android Logcat for diagnostics..."

    adb -s "$SERIAL" logcat -d -t 4000 \
        > artifacts/logcat-on-pytest-failure.txt 2>&1 || true

    exit "$TEST_EXIT_CODE"
fi