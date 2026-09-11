# Aportes manuales de la familia

Esta carpeta es la **bandeja de entrada documental** del Agente Genealógico.

Todo dato nuevo aportado por Juan Pablo, Mario Gerardo, Gabriel José, Diana Farah Mizrahy, Gabriel Rodrigo Martínez u otros familiares puede registrarse aquí antes de incorporarlo a los archivos canónicos de `familias/`.

## Cómo registrar un aporte

Cree un archivo Markdown con un nombre como:

`2026-09-11__mario-gerardo-valderrama-mutis__entrevista.md`

Use, cuando sea posible, esta estructura:

```md
# Aporte familiar

- Persona que aporta la información:
- Relación con la familia/personas mencionadas:
- Fecha de la conversación o documento:
- Tipo: entrevista / recuerdo / fotografía / registro civil / partida / carta / otro

## Transcripción o dato original

Escribir literalmente lo dicho o transcribir el documento sin corregirlo.

## Observaciones

Contexto adicional, dudas, apodos, variantes ortográficas, lugares mencionados, etc.

## Archivos asociados

Nombre de fotografías, documentos o enlaces relacionados.
```

## Qué ocurre después

Cuando un archivo dentro de `aportes-manuales/` llega a `main`, el workflow `Genealogy Research Agent` se activa automáticamente y:

1. extrae las afirmaciones genealógicas;
2. las compara con el corpus actual;
3. busca evidencia pública a favor y en contra;
4. detecta contradicciones y homónimos;
5. asigna nivel A/B/C/D/E/X;
6. genera un informe en una rama independiente;
7. abre una Pull Request para revisión humana.

El agente **no borra ni corrige automáticamente el testimonio original**. La memoria oral queda preservada incluso cuando una fuente secundaria discrepa con ella.

## Regla sobre documentos

Si un aporte procede de un documento primario, transcriba tanto como sea necesario para identificar:

- nombres completos;
- fecha y lugar;
- relación filiatoria;
- institución que expide el documento;
- libro/tomo/folio/número cuando exista.

No publique números de cédula, direcciones privadas, teléfonos, información médica, financiera ni otros datos sensibles innecesarios de personas vivas.
