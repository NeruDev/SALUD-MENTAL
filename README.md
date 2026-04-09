# SALUD-MENTAL

Repositorio de contenido educativo sobre salud mental en español, con generación automatizada de documentación mediante Python y MkDocs.

## Objetivo del repositorio

El proyecto usa `modules/` como fuente de verdad para el contenido educativo.
Ese contenido se transforma automáticamente en el sitio de documentación dentro de `docs/`.

La arquitectura separa:

- contenido fuente en Markdown (`modules/`)
- contenido publicado y navegable (`docs/`)
- automatización y validaciones (`scripts/`)

## Arquitectura actual

### 1) Capa de contenido fuente: `modules/`

Cada carpeta de primer nivel representa un dominio temático de salud mental:

- `fundamentos`
- `bienestar`
- `trastornos`
- `etapas_vida`
- `contexto_social`
- `prevencion`
- `recursos`

### 2) Capa de generación: `scripts/docs/`

`scripts/docs/build_docs.py` ejecuta el pipeline principal:

1. Limpia `docs/`.
2. Copia archivos `.md` desde `modules/` a `docs/` respetando estructura.
3. Regenera `docs/index.md`.
4. Reescribe la sección `nav` en `mkdocs.yml` con `scripts/docs/generate_nav.py`.

### 3) Capa de publicación: MkDocs + GitHub Pages

- `mkdocs.yml` define tema, idioma y navegación.
- `.github/workflows/deploy.yml` construye y publica en GitHub Pages al hacer push en `main`.

### 4) Capa de calidad y convenciones

- `scripts/audit/check_structure.py` valida estructura base.
- `ai/conventions.md` y `ai/guardrails.md` fijan reglas de contenido y cambios.
- `.github/copilot-instructions.md` establece reglas para contribuciones asistidas por IA.

## Flujo de trabajo recomendado

1. Editar contenido en `modules/`.
2. Ejecutar `python scripts/docs/build_docs.py` para regenerar `docs/` y `mkdocs.yml`.
3. Ejecutar `python scripts/audit/check_structure.py` para validar estructura.
4. Publicar cambios (el workflow de GitHub Actions despliega automáticamente).

## Árbol de directorios (ASCII) con función por archivo

```text
SALUD MENTAL/
|-- .gitignore                                # Exclusiones de entorno, cachés y salida de build.
|-- mkdocs.yml                                # Configuración de MkDocs (tema, idioma, navegación).
|-- README.md                                 # Documentación técnica principal del repositorio.
|-- requirements.txt                          # Dependencias de Python para build y despliegue.
|-- .github/
|   |-- copilot-instructions.md               # Reglas para contribuciones asistidas por IA.
|   `-- workflows/
|       `-- deploy.yml                        # Pipeline CI/CD para publicación en GitHub Pages.
|-- ai/
|   |-- conventions.md                        # Convenciones de estructura, nombres y estilo.
|   `-- guardrails.md                         # Restricciones y prácticas obligatorias.
|-- docs/                                     # Salida generada desde modules (no editar manualmente).
|-- modules/                                  # Fuente de verdad del contenido educativo.
|   |-- fundamentos/
|   |   |-- README.md                         # Introducción al marco conceptual de salud mental.
|   |   |-- que_es_salud_mental.md            # Definición, alcance y mitos frecuentes.
|   |   |-- dimensiones.md                    # Dimensiones emocional, cognitiva, social y física.
|   |   `-- factores_riesgo.md                # Riesgos y factores protectores en enfoque biopsicosocial.
|   |-- bienestar/
|   |   |-- README.md                         # Introducción al módulo de bienestar.
|   |   |-- autocuidado.md                    # Principios y prácticas de autocuidado sostenible.
|   |   |-- habitos_saludables.md             # Hábitos diarios con impacto en salud mental.
|   |   `-- regulacion_emocional.md           # Técnicas de regulación emocional y manejo de estrés.
|   |-- trastornos/
|   |   |-- README.md                         # Introducción a trastornos de salud mental frecuentes.
|   |   |-- ansiedad.md                       # Síntomas, tipos, factores y abordaje de ansiedad.
|   |   |-- depresion.md                      # Señales, tipos, riesgos y tratamiento de depresión.
|   |   |-- estres_postraumatico.md           # Bases del TEPT, síntomas y apoyo recomendado.
|   |   `-- adicciones.md                     # Conceptos clave, riesgos y recuperación en adicciones.
|   |-- etapas_vida/
|   |   |-- README.md                         # Introducción al enfoque por ciclo vital.
|   |   |-- infancia.md                       # Necesidades emocionales y señales de alerta en infancia.
|   |   |-- adolescencia.md                   # Retos, factores protectores y acompañamiento adolescente.
|   |   |-- adultez.md                        # Salud mental en contexto de responsabilidades adultas.
|   |   `-- adulto_mayor.md                   # Bienestar emocional, autonomía y redes en vejez.
|   |-- contexto_social/
|   |   |-- README.md                         # Introducción a determinantes sociales del bienestar.
|   |   |-- familia.md                        # Dinámicas familiares de riesgo y protección.
|   |   |-- trabajo.md                        # Factores psicosociales laborales y prevención de desgaste.
|   |   |-- redes_sociales.md                 # Efectos del entorno digital en salud mental.
|   |   `-- cultura.md                        # Estigma, diversidad e influencia cultural en el cuidado.
|   |-- prevencion/
|   |   |-- README.md                         # Introducción a prevención y detección temprana.
|   |   |-- estrategias.md                    # Estrategias preventivas individuales y comunitarias.
|   |   |-- intervenciones.md                 # Intervenciones escalonadas según nivel de riesgo.
|   |   `-- educacion.md                      # Alfabetización y formación en salud mental.
|   `-- recursos/
|       |-- README.md                         # Introducción a recursos de apoyo.
|       |-- ayuda_profesional.md              # Guía para buscar atención profesional.
|       |-- lineas_apoyo.md                   # Líneas de crisis y orientación inmediata.
|       `-- bibliografia.md                   # Fuentes institucionales y lecturas recomendadas.
`-- scripts/
    |-- __init__.py                           # Inicializador del paquete de scripts.
    |-- audit/
    |   |-- __init__.py                       # Inicializador del subpaquete de auditoría.
    |   `-- check_structure.py                # Valida archivos y estructura esperada del repositorio.
    |-- docs/
    |   |-- __init__.py                       # Inicializador del subpaquete de generación de docs.
    |   |-- build_docs.py                     # Pipeline principal de construcción de documentación.
    |   `-- generate_nav.py                   # Genera navegación de MkDocs a partir de modules/docs.
    `-- utils/
        |-- __init__.py                       # Inicializador del subpaquete de utilidades.
        `-- common.py                         # Rutas y utilidades compartidas por scripts.
```

## Nota importante

`docs/` es una carpeta generada automáticamente.
Para mantener coherencia, todo cambio editorial debe hacerse en `modules/` y luego ejecutar los scripts de build.
