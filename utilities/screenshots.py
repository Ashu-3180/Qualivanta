"""Deterministic screenshot output helpers."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


def _safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return cleaned.strip("._") or "screen"


def save_screenshot(driver, name: str, output_dir: str | Path) -> Path:
    """Save a PNG with a descriptive UTC timestamp and return its path."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = directory / f"{_safe_name(name)}_{timestamp}.png"
    if not driver.save_screenshot(str(path)):
        raise RuntimeError(f"Appium did not save a screenshot to {path}.")
    return path
