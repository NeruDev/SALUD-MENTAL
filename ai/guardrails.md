# AI Guardrails

## Forbidden actions

- Mixing content (Markdown) and code (Python) in the same directory.
- Writing files outside their defined folders (e.g., Python in `/modules`).
- Generating or modifying `/docs` files manually.
- Including medical diagnoses, prescriptions, or treatment recommendations in content.
- Using English inside educational Markdown content in `/modules`.

## Required practices

- Make **minimal changes**: only touch files necessary to address the task.
- **Respect the structure**: follow the directory layout defined in `ai/conventions.md`.
- **Review before committing**: run `python scripts/audit/check_structure.py` to validate.
- Attribute sources when reproducing factual health information.
- Always recommend professional support when discussing mental health crises.

## Sensitive content guidance

Mental health content must:

1. Be factually accurate and reviewed against reputable sources (WHO, APA, etc.).
2. Avoid stigmatising language (e.g., prefer "person with depression" over "depressive").
3. Include crisis resources when discussing severe conditions.
4. Use inclusive, gender-neutral language where possible.
