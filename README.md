# Árbol genealógico de Juan Pablo Valderrama Pino

> Una obra en homenaje a mi familia, mi pasado y todas las vidas que he sido a través de cada uno.

Investigación genealógica e histórico-documental sobre las familias **Valderrama, Mutis, Martínez, Cabrales, Pino, Bechara, Farah y Mizrahy** vinculadas a la ascendencia de Juan Pablo Valderrama Pino.

## Objetivo

Reconstruir el árbol genealógico familiar con metodología documental, distinguiendo cuidadosamente entre tradición oral, documentación secundaria, fuentes académicas y documentos primarios. El proyecto presta especial atención a:

- la rama **Valderrama–Ordóñez** de Santander y sus conexiones con Pedro Gómez Valderrama y Augusto Espinosa Valderrama;
- la rama **Mutis** de Bucaramanga/Santander y su relación con Manuel Mutis Bossio, José Celestino Mutis, Álvaro Mutis y Aurelio Martínez Mutis;
- la rama **Martínez–Cabrales** de Zilia Margarita Martínez Cabrales;
- la posible bifurcación **Valderrama de Sopetrán/Antioquia** y su eventual conexión con la familia Valderrama Tobón de Sergio Fajardo;
- la rama materna biológica **Farah–Mizrahy**;
- la rama materna adoptiva **Pino–Bechara**.

## Escala de evidencia

- **A — Fuente primaria:** registro civil, partida sacramental, matrimonio, documento notarial, archivo militar u otro documento contemporáneo verificable.
- **B — Fuentes secundarias concordantes:** publicaciones académicas, genealogías reconocidas, obituarios o archivos históricos independientes.
- **C — Tradición oral familiar directa:** testimonio de descendientes o parientes con conocimiento personal de la relación.
- **D — Hipótesis genealógica fuerte:** coherencia nominal, cronológica y geográfica, pero falta el documento filiatorio decisivo.
- **E — Hipótesis abierta:** tradición, coincidencia o pista todavía sin cadena demostrada.
- **X — Controvertido:** fuentes incompatibles o contradicción no resuelta.

## Organización

- [`PROMPT_MAESTRO.md`](PROMPT_MAESTRO.md): protocolo y megaprompt para continuar la investigación.
- [`familias/README.md`](familias/README.md): índice maestro de personas, ramas y relaciones.
- [`familias/valderrama-ordonez.md`](familias/valderrama-ordonez.md): rama Valderrama, Santander y Sopetrán.
- [`familias/mutis.md`](familias/mutis.md): rama Mutis de Santander y conexión con José Celestino Mutis.
- [`familias/martinez-cabrales.md`](familias/martinez-cabrales.md): ascendencia de Zilia Margarita Martínez Cabrales.
- [`familias/pino-bechara.md`](familias/pino-bechara.md): filiación adoptiva materna.
- [`familias/farah-mizrahy.md`](familias/farah-mizrahy.md): filiación biológica materna.
- [`familias/conexiones-literarias.md`](familias/conexiones-literarias.md): parentescos culturales y literarios.
- [`familias/fajardo-valderrama.md`](familias/fajardo-valderrama.md): hipótesis Valderrama Tobón de Antioquia.
- [`entrevistas/cuestionarios.md`](entrevistas/cuestionarios.md): historia oral en curso.
- [`fuentes/README.md`](fuentes/README.md): fuentes utilizadas y documentos prioritarios por localizar.
- [`aportes-manuales/`](aportes-manuales/): bandeja de entrada para nueva información familiar.
- [`agent/`](agent/): agente autónomo de investigación y validación.
- `investigacion/agente/`: informes generados automáticamente por el agente.

## Agente de IA para investigación genealógica

El repositorio incorpora un **Agente Genealógico auditable** que ejecuta dos funciones permanentes:

1. **Investigación autónoma:** realiza rondas periódicas de búsqueda web sobre las ramas y eslabones prioritarios definidos en `agent/research_queue.json`.
2. **Validación de aportes:** cuando se agrega o modifica información familiar, el agente extrae las afirmaciones, las compara con el corpus, busca evidencia a favor y en contra, detecta contradicciones y asigna nivel A/B/C/D/E/X.

El agente está deliberadamente diseñado para **no reescribir por sí solo el árbol canónico**. Cada ejecución produce un informe en una rama separada y abre una Pull Request para revisión humana. De esta manera, ninguna hipótesis se transforma silenciosamente en un hecho genealógico.

Documentación técnica: [`agent/README.md`](agent/README.md).

### Activación

El workflow `.github/workflows/genealogy-agent.yml` se ejecuta:

- dos veces al día;
- cuando cambian archivos genealógicos o aportes manuales relevantes;
- manualmente mediante `workflow_dispatch`.

Para funcionar necesita el secreto de GitHub Actions `OPENAI_API_KEY`. El modelo puede configurarse opcionalmente mediante la variable `OPENAI_MODEL`; de forma predeterminada se utiliza `gpt-5.6-terra`.

## Núcleo familiar de partida

**Juan Pablo Valderrama Pino** (Cartagena de Indias, 1992), hijo de:

- **Gabriel José Valderrama Martínez**, hijo biológico de Mario Gerardo Valderrama Mutis y Zilia Margarita Martínez Cabrales.
- **María del Rosario Pino Bechara**, hija adoptiva de Marco Tulio Pino Uribe y Hortensia Bechara Kahtouny, e hija biológica de Diana Farah Mizrahy.

## Regla editorial

Este repositorio es una investigación en curso. Ningún parentesco debe considerarse probado únicamente por coincidencia de apellidos o por árboles digitales sin documentación. La meta es sustituir progresivamente las afirmaciones de niveles C–E por documentación primaria de nivel A siempre que sea posible.
