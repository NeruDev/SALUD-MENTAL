"""Common utilities shared across scripts."""

from __future__ import annotations

import os
from pathlib import Path

# Project root is two levels above this file (scripts/utils/common.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = PROJECT_ROOT / "modules"
DOCS_DIR = PROJECT_ROOT / "docs"


def get_module_dirs() -> list[Path]:
    """Return all subdirectory paths inside /modules."""
    return sorted(
        [d for d in MODULES_DIR.iterdir() if d.is_dir()],
        key=lambda p: p.name,
    )


def ensure_dir(path: Path) -> None:
    """Create *path* (and parents) if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def relative_to_root(path: Path) -> str:
    """Return *path* as a string relative to the project root."""
    return str(path.relative_to(PROJECT_ROOT))


def is_markdown(path: Path) -> bool:
    """Return True if *path* is a Markdown file."""
    return path.suffix.lower() == ".md"


def print_ok(message: str) -> None:
    print(f"  ✅  {message}")


def print_warn(message: str) -> None:
    print(f"  ⚠️  {message}")


def print_error(message: str) -> None:
    print(f"  ❌  {message}")
