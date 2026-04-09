"""Validate the repository structure against the expected conventions.

Usage:
    python scripts/audit/check_structure.py

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow importing from scripts/utils when run directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.utils.common import (
    DOCS_DIR,
    MODULES_DIR,
    PROJECT_ROOT,
    get_module_dirs,
    is_markdown,
    print_error,
    print_ok,
    print_warn,
    relative_to_root,
)

REQUIRED_ROOT_FILES = [
    "mkdocs.yml",
    "requirements.txt",
    "README.md",
    ".gitignore",
]

REQUIRED_MODULE_FILES = ["README.md"]


def check_root_files() -> list[str]:
    """Verify required root-level files exist."""
    errors: list[str] = []
    for filename in REQUIRED_ROOT_FILES:
        path = PROJECT_ROOT / filename
        if path.exists():
            print_ok(f"Root file exists: {filename}")
        else:
            msg = f"Missing required root file: {filename}"
            print_error(msg)
            errors.append(msg)
    return errors


def check_modules_dir() -> list[str]:
    """Verify /modules exists and each module has the required files."""
    errors: list[str] = []

    if not MODULES_DIR.exists():
        msg = "Missing /modules directory"
        print_error(msg)
        return [msg]

    module_dirs = get_module_dirs()
    if not module_dirs:
        msg = "/modules directory is empty — no modules found"
        print_warn(msg)
        errors.append(msg)

    for module_dir in module_dirs:
        for required in REQUIRED_MODULE_FILES:
            required_path = module_dir / required
            if required_path.exists():
                print_ok(f"Module file exists: {relative_to_root(required_path)}")
            else:
                msg = f"Missing {required} in module '{module_dir.name}'"
                print_error(msg)
                errors.append(msg)

        # No Python files allowed inside /modules
        for item in module_dir.rglob("*.py"):
            msg = f"Python file found inside /modules (forbidden): {relative_to_root(item)}"
            print_error(msg)
            errors.append(msg)

    return errors


def check_modules_only_markdown() -> list[str]:
    """Verify /modules contains ONLY Markdown files (ignoring directories and hidden files)."""
    errors: list[str] = []
    for item in MODULES_DIR.rglob("*"):
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if not is_markdown(item):
            msg = f"Non-Markdown file in /modules: {relative_to_root(item)}"
            print_error(msg)
            errors.append(msg)
    return errors


def check_docs_dir() -> list[str]:
    """Verify /docs/index.md exists (i.e., build_docs.py has been run)."""
    errors: list[str] = []
    index = DOCS_DIR / "index.md"
    if index.exists():
        print_ok("docs/index.md exists")
    else:
        msg = "docs/index.md missing — run 'python scripts/docs/build_docs.py' first"
        print_warn(msg)
        # This is a warning rather than hard error since docs are auto-generated
    return errors


def check_scripts_no_markdown_content() -> list[str]:
    """Verify /scripts contains no Markdown content files (only .py)."""
    scripts_dir = PROJECT_ROOT / "scripts"
    errors: list[str] = []
    for item in scripts_dir.rglob("*.md"):
        msg = f"Markdown file found inside /scripts (unexpected): {relative_to_root(item)}"
        print_warn(msg)
        # Not a hard error but worth flagging
    return errors


def main() -> int:
    print("🔍 Checking repository structure ...\n")

    all_errors: list[str] = []

    print("── Root files ──")
    all_errors += check_root_files()

    print("\n── Modules directory ──")
    all_errors += check_modules_dir()
    all_errors += check_modules_only_markdown()

    print("\n── Docs directory ──")
    all_errors += check_docs_dir()

    print("\n── Scripts directory ──")
    all_errors += check_scripts_no_markdown_content()

    print()
    if all_errors:
        print(f"❌ Structure check FAILED — {len(all_errors)} error(s) found:")
        for err in all_errors:
            print(f"   • {err}")
        return 1

    print("✅ All structure checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
