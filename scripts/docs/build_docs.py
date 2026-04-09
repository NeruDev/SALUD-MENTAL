"""Copy content from /modules into /docs and regenerate mkdocs.yml navigation.

Usage:
    python scripts/docs/build_docs.py

What it does:
1. Clears and recreates /docs (except .gitkeep).
2. Copies every .md file from /modules/**/ to the matching path inside /docs/.
3. Generates /docs/index.md as the site landing page.
4. Rewrites the nav: section of mkdocs.yml to reflect the current content.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml

# Allow importing from scripts/utils when run directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.docs.generate_nav import build_nav
from scripts.utils.common import (
    DOCS_DIR,
    MODULES_DIR,
    PROJECT_ROOT,
    ensure_dir,
    get_module_dirs,
    is_markdown,
    print_error,
    print_ok,
    print_warn,
    relative_to_root,
)

MKDOCS_YML = PROJECT_ROOT / "mkdocs.yml"
STYLESHEETS_DIR = PROJECT_ROOT / "stylesheets"
DOCS_STYLESHEETS_DIR = DOCS_DIR / "stylesheets"

INDEX_TEMPLATE = """\
# Salud Mental — Documentación Educativa

Bienvenido al sitio educativo sobre salud mental.

Este recurso ha sido creado con el objetivo de brindar información clara,
accesible y responsable sobre temas de salud mental.

## Módulos disponibles

{module_list}

---

> ⚠️ **Aviso**: El contenido de este sitio tiene fines educativos únicamente
> y no reemplaza la atención de un profesional de la salud mental.
"""

MODULE_DESCRIPTIONS: dict[str, str] = {
    "fundamentos": "Conceptos base para comprender la salud mental y sus dimensiones.",
    "bienestar": "Hábitos y prácticas para cuidar el bienestar emocional en la vida diaria.",
    "trastornos": "Panorama educativo de trastornos frecuentes y rutas de apoyo.",
    "etapas_vida": "Retos y factores protectores de salud mental según el ciclo vital.",
    "contexto_social": "Impacto de familia, trabajo, redes y cultura en la salud mental.",
    "prevencion": "Estrategias e intervenciones para prevención y detección temprana.",
    "recursos": "Guías de ayuda profesional, líneas de apoyo y bibliografía confiable.",
}


def _clean_docs_dir() -> None:
    """Remove all content inside /docs but keep the directory itself."""
    if DOCS_DIR.exists():
        for item in DOCS_DIR.iterdir():
            if item.name == ".gitkeep":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        DOCS_DIR.mkdir(parents=True)


def _copy_modules() -> list[str]:
    """Copy .md files from /modules to /docs, preserving structure.

    Returns a list of module names that were successfully copied.
    """
    copied_modules: list[str] = []

    for module_dir in get_module_dirs():
        md_files = [f for f in module_dir.iterdir() if is_markdown(f)]
        if not md_files:
            print_warn(f"Module '{module_dir.name}' has no .md files — skipping.")
            continue

        dest_dir = DOCS_DIR / module_dir.name
        ensure_dir(dest_dir)

        for md_file in md_files:
            dest_file = dest_dir / md_file.name
            shutil.copy2(md_file, dest_file)
            print_ok(f"Copied {relative_to_root(md_file)} → {relative_to_root(dest_file)}")

        copied_modules.append(module_dir.name)

    return copied_modules


def _generate_index(module_names: list[str]) -> None:
    """Write /docs/index.md with links to each module."""
    lines: list[str] = []
    for name in sorted(module_names):
        desc = MODULE_DESCRIPTIONS.get(name, "")
        label = name.replace("_", " ").title()
        lines.append(f"- [{label}]({name}/README.md): {desc}")

    index_content = INDEX_TEMPLATE.format(module_list="\n".join(lines))
    index_path = DOCS_DIR / "index.md"
    index_path.write_text(index_content, encoding="utf-8")
    print_ok(f"Generated {relative_to_root(index_path)}")


def _copy_stylesheets() -> None:
    """Copy custom CSS files from /stylesheets into /docs/stylesheets."""
    if not STYLESHEETS_DIR.exists():
        print_warn("stylesheets directory not found — skipping CSS copy.")
        return

    ensure_dir(DOCS_STYLESHEETS_DIR)

    css_files = sorted(STYLESHEETS_DIR.glob("*.css"))
    if not css_files:
        print_warn("No .css files found in stylesheets — skipping CSS copy.")
        return

    for css_file in css_files:
        dest_file = DOCS_STYLESHEETS_DIR / css_file.name
        shutil.copy2(css_file, dest_file)
        print_ok(f"Copied {relative_to_root(css_file)} → {relative_to_root(dest_file)}")


def _update_mkdocs_nav(nav: list[dict]) -> None:
    """Replace the nav: section in mkdocs.yml with the generated navigation."""
    if not MKDOCS_YML.exists():
        print_error(f"{MKDOCS_YML} not found — skipping nav update.")
        return

    yaml_text = MKDOCS_YML.read_text(encoding="utf-8")
    config = yaml.safe_load(yaml_text)
    config["nav"] = nav

    MKDOCS_YML.write_text(
        yaml.dump(config, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print_ok("Updated nav section in mkdocs.yml")


def main() -> None:
    print("🔨 Building docs from modules ...\n")

    print("→ Cleaning /docs directory ...")
    _clean_docs_dir()

    print("\n→ Copying modules to /docs ...")
    copied_modules = _copy_modules()

    if not copied_modules:
        print_error("No modules were copied. Aborting.")
        sys.exit(1)

    print("\n→ Copying stylesheets to /docs ...")
    _copy_stylesheets()

    print("\n→ Generating index.md ...")
    _generate_index(copied_modules)

    print("\n→ Updating mkdocs.yml navigation ...")
    nav = build_nav()
    _update_mkdocs_nav(nav)

    print("\n✅ Build complete.")


if __name__ == "__main__":
    main()
