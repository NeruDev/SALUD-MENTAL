# SALUD-MENTAL

Repositorio de contenido educativo sobre salud mental en espanol, con generacion automatizada de documentacion mediante Python y MkDocs.

## Objetivo del repositorio

Este proyecto organiza contenido educativo en Markdown dentro de `modules/` y lo publica como sitio estatico con MkDocs.

La arquitectura separa claramente:

- contenido fuente (`modules/`)
- contenido publicado (`docs/`, generado automaticamente)
- automatizacion y validaciones (`scripts/`)

## Arquitectura actual

### 1) Capa de contenido fuente: `modules/`

`modules/` es la fuente de verdad del contenido educativo. Cada carpeta representa un modulo tematico y debe incluir al menos un `README.md`.

Modulos actuales:

- `ansiedad`: introduccion, teoria y ejercicios practicos.
- `bienestar`: fundamentos y habitos de bienestar mental.
- `depresion`: introduccion, teoria y recursos de apoyo.

### 2) Capa de generacion: `scripts/docs/`

El script `scripts/docs/build_docs.py` implementa el pipeline de construccion:

1. Limpia `docs/`.
2. Copia los `.md` desde `modules/` hacia `docs/` respetando estructura.
3. Regenera `docs/index.md`.
4. Reescribe la seccion `nav` en `mkdocs.yml` con `scripts/docs/generate_nav.py`.

### 3) Capa de publicacion: MkDocs + GitHub Pages

- `mkdocs.yml` define tema, idioma y navegacion del sitio.
- `.github/workflows/deploy.yml` ejecuta en cada push a `main`:
	- instalacion de dependencias,
	- build desde `modules/`,
	- despliegue con `mkdocs gh-deploy --force`.

### 4) Capa de calidad y convenciones

- `scripts/audit/check_structure.py` valida estructura y reglas base.
- `ai/conventions.md` y `ai/guardrails.md` documentan convenciones y restricciones.
- `.github/copilot-instructions.md` fija reglas para contribuciones asistidas por IA.

## Flujo de trabajo recomendado

1. Editar o crear contenido en `modules/`.
2. Ejecutar `python scripts/docs/build_docs.py` para regenerar `docs/` y `mkdocs.yml` (nav).
3. Ejecutar `python scripts/audit/check_structure.py` para validar estructura.
4. Publicar cambios (el workflow de GitHub Actions despliega en Pages).

## Arbol de directorios (ASCII) con funcion por archivo

```text
SALUD MENTAL/
|-- .gitignore                          # Ignora venv, caches, salida de MkDocs y archivos de editor.
|-- mkdocs.yml                          # Configuracion principal de MkDocs (tema, idioma, nav).
|-- README.md                           # Documentacion tecnica del repositorio (este archivo).
|-- requirements.txt                    # Dependencias Python para build y despliegue de docs.
|-- .github/
|   |-- copilot-instructions.md         # Reglas de contribucion asistida por IA para este repo.
|   `-- workflows/
|       `-- deploy.yml                  # CI/CD: construye docs desde modules y publica en GitHub Pages.
|-- ai/
|   |-- conventions.md                  # Convenciones de estructura, nombres y estilo de contenido.
|   `-- guardrails.md                   # Restricciones y practicas obligatorias para cambios.
|-- docs/                               # Salida generada para MkDocs (no editar manualmente).
|   |-- index.md                        # Portada del sitio, autogenerada por build_docs.py.
|   |-- ansiedad/
|   |   |-- ejercicios.md               # Copia generada desde modules/ansiedad/ejercicios.md.
|   |   |-- README.md                   # Copia generada desde modules/ansiedad/README.md.
|   |   `-- teoria.md                   # Copia generada desde modules/ansiedad/teoria.md.
|   |-- bienestar/
|   |   `-- README.md                   # Copia generada desde modules/bienestar/README.md.
|   `-- depresion/
|       |-- README.md                   # Copia generada desde modules/depresion/README.md.
|       |-- recursos.md                 # Copia generada desde modules/depresion/recursos.md.
|       `-- teoria.md                   # Copia generada desde modules/depresion/teoria.md.
|-- modules/                            # Fuente de verdad del contenido educativo en Markdown.
|   |-- ansiedad/
|   |   |-- ejercicios.md               # Tecnicas practicas para gestionar ansiedad.
|   |   |-- README.md                   # Introduccion del modulo de ansiedad.
|   |   `-- teoria.md                   # Fundamentos y tipos de ansiedad.
|   |-- bienestar/
|   |   `-- README.md                   # Habitos y practicas para bienestar mental.
|   `-- depresion/
|       |-- README.md                   # Introduccion del modulo de depresion.
|       |-- recursos.md                 # Recursos de apoyo, lecturas y lineas de ayuda.
|       `-- teoria.md                   # Bases teoricas, tipos y tratamiento de depresion.
`-- scripts/                            # Automatizacion del proyecto (solo Python).
		|-- __init__.py                     # Marca scripts como paquete Python.
		|-- audit/
		|   |-- __init__.py                 # Inicializador del subpaquete de auditoria.
		|   `-- check_structure.py          # Valida estructura, archivos requeridos y reglas de contenido.
		|-- docs/
		|   |-- __init__.py                 # Inicializador del subpaquete de generacion de docs.
		|   |-- build_docs.py               # Pipeline principal: limpia, copia modules, crea index y actualiza nav.
		|   `-- generate_nav.py             # Construye la estructura nav de mkdocs.yml desde docs/.
		`-- utils/
				|-- __init__.py                 # Inicializador del subpaquete de utilidades.
				`-- common.py                   # Rutas base, helpers y funciones compartidas de consola.
```

## Nota importante

La carpeta `docs/` es generada automaticamente desde `modules/`. Para mantener coherencia y trazabilidad, los cambios de contenido deben hacerse en `modules/` y luego regenerar la documentacion con los scripts del proyecto.
