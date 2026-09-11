# Agente de Investigación Genealógica

Este directorio implementa un agente de IA para investigación continua y validación de la genealogía de Juan Pablo Valderrama Pino.

## Qué hace

### Investigación periódica

Dos veces al día el workflow selecciona un tema de `research_queue.json`, carga el corpus genealógico del repositorio y ejecuta una investigación web enfocada en encontrar:

- documentos primarios;
- nuevas filiaciones candidatas;
- fechas y lugares;
- obituarios y prensa histórica;
- archivos académicos e institucionales;
- contradicciones;
- homónimos;
- fuentes que refuten hipótesis existentes.

### Validación de aportes manuales

Los cambios en:

- `aportes-manuales/**`
- `familias/**`
- `entrevistas/**`
- `fuentes/**`
- `PROMPT_MAESTRO.md`

activan una auditoría automática. El agente examina el diff, extrae afirmaciones atómicas y las coteja contra el repositorio y la web.

### Revisión humana obligatoria

El agente **no modifica directamente los archivos canónicos de `familias/`**. Cada ejecución genera un archivo dentro de `investigacion/agente/` en una rama independiente y abre una Pull Request.

La PR debe revisarse antes de que cualquier conclusión sea incorporada al árbol.

## Arquitectura

- `SYSTEM_PROMPT.md`: constitución epistemológica del agente.
- `genealogy_agent.py`: motor de investigación y validación.
- `research_queue.json`: temas rotativos de investigación.
- `requirements.txt`: dependencia del SDK de OpenAI.
- `.github/workflows/genealogy-agent.yml`: ejecución programada y por eventos.
- `aportes-manuales/`: bandeja de entrada de testimonios y documentos familiares.
- `investigacion/agente/`: informes generados automáticamente.

## Modelo

Por defecto se usa `gpt-5.6-terra`, seleccionado para equilibrar capacidad de razonamiento y costo. Puede sustituirse mediante la variable de repositorio `OPENAI_MODEL` sin modificar código.

La implementación utiliza la Responses API con la herramienta de búsqueda web y solicita las fuentes estructuradas de cada búsqueda. Las respuestas API se ejecutan con `store=False`.

## Configuración manual obligatoria

GitHub debe disponer del secreto:

`OPENAI_API_KEY`

Ruta en GitHub:

**Settings → Secrets and variables → Actions → New repository secret**

Nombre: `OPENAI_API_KEY`

Valor: una API key válida de OpenAI con facturación/cuota suficiente.

Opcionalmente, en **Settings → Secrets and variables → Actions → Variables**, puede crearse:

`OPENAI_MODEL=gpt-5.6-terra`

Sin `OPENAI_API_KEY` el workflow falla deliberadamente antes de investigar.

## Frecuencia

El agente se ejecuta a las **05:17 y 17:17, hora de Colombia (`America/Bogota`)**. Se evita el inicio exacto de la hora porque los workflows programados de GitHub pueden sufrir mayor retraso en momentos de alta carga.

También puede ejecutarse desde **Actions → Genealogy Research Agent → Run workflow** en tres modos:

- `research`: nueva ronda de investigación;
- `validate`: valida el cambio más reciente;
- `full`: validación + investigación.

Puede indicarse un `topic` específico usando uno de los `id` definidos en `research_queue.json`.

## Límites deliberados

El agente no debe:

- afirmar parentescos únicamente por coincidencia de apellidos;
- autopromover hipótesis a evidencia A;
- ocultar contradicciones;
- borrar testimonios familiares porque contradigan una base web;
- publicar información sensible innecesaria de personas vivas;
- incorporar directamente hallazgos al árbol sin revisión humana.

## Flujo recomendado para nueva información familiar

1. Añadirla a `aportes-manuales/` conservando el testimonio literal.
2. Hacer commit/push a `main`.
3. Esperar el informe automático de validación.
4. Revisar la PR y sus fuentes.
5. Si la evidencia lo permite, actualizar el archivo correspondiente de `familias/` en una PR separada o en la misma revisión humana.
