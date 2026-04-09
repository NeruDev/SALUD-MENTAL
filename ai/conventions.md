# Conventions

## Directory conventions

| Directory | Purpose | Language |
|-----------|---------|----------|
| `/modules` | Educational content | Markdown (Spanish) |
| `/scripts` | Automation and tooling | Python (English) |
| `/docs` | MkDocs input (auto-generated) | Markdown |
| `/ai` | AI instructions and guardrails | English |

## Naming conventions

- Directories and file names: lowercase English, underscores for spaces (e.g., `build_docs.py`).
- Module folder names: lowercase Spanish word (e.g., `ansiedad`, `depresion`, `bienestar`).
- Python functions and variables: `snake_case`.
- Python classes: `PascalCase`.

## Content conventions

- Every module in `/modules` must have a `README.md` as its entry point.
- Markdown files use H1 for the title, H2 for sections.
- Tables are used to compare or list structured information.
- All content is written in the second person (tú/usted implied) and maintains an empathetic, non-judgmental tone.

## Script conventions

- Scripts are executable via `python scripts/<subdir>/<script>.py`.
- Common helpers live in `scripts/utils/common.py`.
- Scripts print progress with ✅ (ok), ⚠️ (warning), and ❌ (error) prefixes.
- Scripts exit with code 0 on success and 1 on failure.
