"""Generate the MkDocs navigation section from the /modules directory.

Usage:
    python scripts/docs/generate_nav.py

Outputs a YAML-compatible nav block to stdout, which can be embedded inside
mkdocs.yml by build_docs.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow importing from scripts/utils when run directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.utils.common import (
    DOCS_DIR,
    MODULES_DIR,
    get_module_dirs,
    is_markdown,
    print_ok,
)

# Human-readable labels for known module folders
MODULE_LABELS: dict[str, str] = {
    "fundamentos": "Fundamentos",
    "bienestar": "Bienestar",
    "trastornos": "Trastornos",
    "etapas_vida": "Etapas de Vida",
    "contexto_social": "Contexto Social",
    "prevencion": "Prevención",
    "recursos": "Recursos",
}

# Human-readable labels for known filenames (without extension)
FILE_LABELS: dict[str, str] = {
    "README": "Introducción",
    "que_es_salud_mental": "Qué es la salud mental",
    "dimensiones": "Dimensiones",
    "factores_riesgo": "Factores de riesgo",
    "autocuidado": "Autocuidado",
    "habitos_saludables": "Hábitos saludables",
    "regulacion_emocional": "Regulación emocional",
    "ansiedad": "Ansiedad",
    "depresion": "Depresión",
    "estres_postraumatico": "Estrés postraumático",
    "adicciones": "Adicciones",
    "infancia": "Infancia",
    "adolescencia": "Adolescencia",
    "adultez": "Adultez",
    "adulto_mayor": "Adulto mayor",
    "familia": "Familia",
    "trabajo": "Trabajo",
    "redes_sociales": "Redes sociales",
    "cultura": "Cultura",
    "estrategias": "Estrategias",
    "intervenciones": "Intervenciones",
    "educacion": "Educación",
    "ayuda_profesional": "Ayuda profesional",
    "lineas_apoyo": "Líneas de apoyo",
    "bibliografia": "Bibliografía",
}


def _file_label(stem: str) -> str:
    return FILE_LABELS.get(stem, stem.replace("_", " ").title())


def build_nav() -> list[dict]:
    """Build the nav structure as a list suitable for YAML serialisation."""
    nav: list[dict] = [{"Inicio": "index.md"}]

    for module_dir in get_module_dirs():
        module_name = module_dir.name
        label = MODULE_LABELS.get(module_name, module_name.replace("_", " ").title())

        # Collect .md files that were copied to docs/
        docs_module_dir = DOCS_DIR / module_name
        if not docs_module_dir.exists():
            continue

        entries: list[dict] = []
        for md_file in sorted(docs_module_dir.iterdir()):
            if not is_markdown(md_file):
                continue
            stem = md_file.stem
            file_label = _file_label(stem)
            rel_path = f"{module_name}/{md_file.name}"
            entries.append({file_label: rel_path})

        if entries:
            nav.append({label: entries})

    return nav


def nav_to_yaml(nav: list[dict], indent: int = 0) -> str:
    """Serialise the nav structure to YAML-compatible text."""
    lines: list[str] = []
    prefix = "  " * indent
    for item in nav:
        for key, value in item.items():
            if isinstance(value, str):
                lines.append(f"{prefix}- {key}: {value}")
            elif isinstance(value, list):
                lines.append(f"{prefix}- {key}:")
                lines.append(nav_to_yaml(value, indent + 1))
    return "\n".join(lines)


def main() -> None:
    nav = build_nav()
    yaml_block = nav_to_yaml(nav)
    print(yaml_block)
    print_ok("Navigation generated successfully.")


if __name__ == "__main__":
    main()
