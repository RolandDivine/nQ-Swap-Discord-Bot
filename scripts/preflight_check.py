#!/usr/bin/env python3
"""Enterprise preflight checks for nQ-Swap Discord bot."""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOT_FILE = ROOT / "bot.py"
ENV_FILE = ROOT / "env.example"

REQUIRED_ENV_KEYS = {
    "DISCORD_TOKEN",
    "CHANNEL_ID",
    "GUILD_ID",
}


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode, output


def check_python_syntax() -> list[str]:
    errors: list[str] = []
    try:
        ast.parse(BOT_FILE.read_text(encoding="utf-8"), filename=str(BOT_FILE))
    except SyntaxError as exc:
        errors.append(f"bot.py syntax error: {exc}")
    return errors


def check_required_env_example_keys() -> list[str]:
    errors: list[str] = []
    content = ENV_FILE.read_text(encoding="utf-8")
    keys = set(re.findall(r"^([A-Z0-9_]+)=", content, flags=re.MULTILINE))
    missing = sorted(REQUIRED_ENV_KEYS - keys)
    if missing:
        errors.append(f"env.example missing required keys: {', '.join(missing)}")
    return errors


def check_suspicious_token_patterns() -> list[str]:
    warnings: list[str] = []
    content = BOT_FILE.read_text(encoding="utf-8")
    if re.search(r"DISCORD_TOKEN\s*=\s*['\"][^'\"]+['\"]", content):
        warnings.append("Potential hardcoded DISCORD_TOKEN assignment detected in bot.py")
    return warnings


def check_git_cleanliness() -> list[str]:
    warnings: list[str] = []
    code, output = run(["git", "status", "--short"])
    if code != 0:
        warnings.append(f"git status failed: {output}")
    elif output:
        warnings.append("Working tree is not clean (expected during active development).")
    return warnings


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_python_syntax())
    errors.extend(check_required_env_example_keys())
    warnings.extend(check_suspicious_token_patterns())
    warnings.extend(check_git_cleanliness())

    print("=== nQ-Swap enterprise preflight report ===")
    if errors:
        print("\n[FAILURES]")
        for item in errors:
            print(f"- {item}")

    if warnings:
        print("\n[WARNINGS]")
        for item in warnings:
            print(f"- {item}")

    if not errors and not warnings:
        print("All checks passed.")
    elif not errors:
        print("\nNo blocking failures found.")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
