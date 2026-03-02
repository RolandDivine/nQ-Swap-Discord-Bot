#!/usr/bin/env python3
"""Run nQ-Swap bot with preflight runtime checks."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"

REQUIRED_PACKAGES = {
    "discord": "discord.py",
    "aiohttp": "aiohttp",
    "dotenv": "python-dotenv",
}
REQUIRED_ENV_KEYS = ["DISCORD_TOKEN", "CHANNEL_ID", "GUILD_ID"]


def package_missing(module: str) -> bool:
    return importlib.util.find_spec(module) is None


def _clean_env_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
        cleaned = cleaned[1:-1]
    return cleaned.strip()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    from dotenv import dotenv_values

    for key, value in dotenv_values(path).items():
        if value is None:
            continue
        cleaned = _clean_env_value(value)
        if cleaned:
            os.environ.setdefault(key, cleaned)


def main() -> int:
    missing = [pkg for mod, pkg in REQUIRED_PACKAGES.items() if package_missing(mod)]
    if missing:
        print("❌ Missing runtime dependencies:")
        for pkg in missing:
            print(f" - {pkg}")
        print("Install them with: python -m pip install -r requirements.txt")
        return 1

    load_env_file(ENV_PATH)
    missing_env = [k for k in REQUIRED_ENV_KEYS if not _clean_env_value(os.getenv(k))]
    if missing_env:
        print("❌ Missing required environment variables:")
        for key in missing_env:
            print(f" - {key}")
        print("Create .env from env.example and populate required values.")
        return 1

    if os.getenv("DISCORD_TOKEN", "").startswith(("\"", "'")):
        print("⚠️ DISCORD_TOKEN appears to include literal quotes; verify your .env formatting.")

    print("✅ Runtime prechecks passed. Starting bot...")
    proc = subprocess.run([sys.executable, "bot.py"], cwd=ROOT)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
