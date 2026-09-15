# Agente de Investigación Genealógica

Este directorio implementa un agente de IA para investigación continua y validación de la genealogía de Juan Pablo Valderrama Pino.

> **Principio editorial:** el agente investiga, contrasta y propone. **No es autor del libro y no aprueba capítulos.** El producto final será una obra de autoría humana apoyada en investigación genealógica e histórica documentada y auditada con asistencia de IA. Véase [`../AUTORIA_Y_REVISION.md`](../AUTORIA_Y_REVISION.md).

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

### Foco activo Martínez–Cabrales

Tras el cierre narrativo de la fase Valderrama, el frente prioritario de investigación pasa a la línea de **Zilia Margarita Martínez Cabrales**.

Se añadió una cola específica:

- [`research_queue_martinez_cabrales_2026-09-14.json`](research_queue_martinez_cabrales_2026-09-14.json)

Esta cola no sustituye automáticamente a `research_queue.json`: funciona como **plan de investigación focal** hasta que la cola general sea reconciliada en una revisión posterior. Sus objetivos P0 incluyen:

- nacimiento/bautismo de Zilia;
- matrimonio Gabriel María Martínez Lugo × Zoila Margarita Cabrales Pineda;
- partida matrimonial de José Casiano Martínez Maijel;
- reconstrucción Martínez–Lora–Sossa en Lorica;
- matrimonio Cabrales–Armesto de Ocaña en 1802;
- bautismo de Manuel José de la Trinidad Cabrales de Armesto en 1810;
- alcaldía de Ignacio José Cabrales González en 1932;
- registros de la línea Pineda–Vélez.

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

Del mismo modo, un hallazgo incorporado a `textos/` debe permanecer rotulado como **borrador asistido por IA** hasta que el autor lo revise, reescriba cuando corresponda y lo apruebe expresamente.

## Arquitectura

- `SYSTEM_PROMPT.md`: constitución epistemológica del agente.
- `genealogy_agent.py`: motor de investigación y validación.
- `research_queue.json`: temas rotativos de investigación general.
- `research_queue_martinez_cabrales_2026-09-14.json`: foco documental Martínez–Cabrales vigente.
- `requirements.txt`: dependencia del SDK de OpenAI.
- `.github/workflows/genealogy-agent.yml`: ejecución programada y por eventos.
- `aportes-manuales/`: bandeja de entrada de testimonios y documentos familiares.
- `investigacion/agente/`: informes generados automáticamente.

## Modelo

La configuración concreta del modelo se controla mediante la variable de repositorio `OPENAI_MODEL`. La documentación del agente no debe utilizar el nombre de un modelo como parte de la metodología permanente, porque los modelos disponibles pueden cambiar. La selección debe privilegiar capacidad de razonamiento, trazabilidad de fuentes y costo compatible con la frecuencia del workflow.

La implementación utiliza la Responses API con la herramienta de búsqueda web y solicita las fuentes estructuradas de cada búsqueda. Las respuestas API se ejecutan con `store=False`.

## Configuración manual obligatoria

GitHub debe disponer del secreto:

`OPENAI_API_KEY`

Ruta en GitHub:

**Settings → Secrets and variables → Actions → New repository secret**

Nombre: `OPENAI_API_KEY`

Valor: una API key válida de OpenAI con facturación/cuota suficiente.

Opcionalmente, en **Settings → Secrets and variables → Actions → Variables**, puede definirse `OPENAI_MODEL` con un modelo compatible con la implementación vigente.

Sin `OPENAI_API_KEY` el workflow falla deliberadamente antes de investigar.

## Frecuencia

El agente se ejecuta a las **05:17 y 17:17, hora de Colombia (`America/Bogota`)**. Se evita el inicio exacto de la hora porque los workflows programados de GitHub pueden sufrir mayor retraso en momentos de alta carga.

También puede ejecutarse desde **Actions → Genealogy Research Agent → Run workflow** en tres modos:

- `research`: nueva ronda de investigación;
- `validate`: valida el cambio más reciente;
- `full`: validación + investigación.

Puede indicarse un `topic` específico usando uno de los `id` definidos en la cola general. Los tópicos del foco Martínez–Cabrales deben incorporarse a la cola general o ejecutarse mediante una adaptación explícita del workflow antes de asumir que el agente los seleccionará automáticamente.

## Límites deliberados

El agente no debe:

- afirmar parentescos únicamente por coincidencia de apellidos;
- autopromover hipótesis a evidencia A;
- ocultar contradicciones;
- borrar testimonios familiares porque contradigan una base web;
- publicar información sensible innecesaria de personas vivas;
- incorporar directamente hallazgos al árbol sin revisión humana;
- presentar borradores generados por IA como capítulos definitivos;
- atribuirse autoría sobre el manuscrito final.

## Flujo recomendado para nueva información familiar

1. Añadirla a `aportes-manuales/` conservando el testimonio literal.
2. Hacer commit/push a `main`.
3. Esperar el informe automático de validación.
4. Revisar la PR y sus fuentes.
5. Si la evidencia lo permite, actualizar el archivo correspondiente de `familias/` en una PR separada o en la misma revisión humana.
6. Si el hallazgo afecta un capítulo, actualizar el borrador manteniendo estado `IA-DRAFT` hasta revisión y aprobación del autor.
