#!/usr/bin/env python3
"""Agente genealógico auditable.

Modos:
- research: investiga un tema rotativo de la cola con búsqueda web.
- validate: revisa cambios/aportes manuales contra el corpus y la web.
- full: ejecuta validación (si hay diff) e investigación.

El agente NO modifica archivos canónicos de familias. Solo genera informes que
se someten a revisión humana mediante Pull Request.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "agent"
REPORTS_DIR = ROOT / "investigacion" / "agente"
DEFAULT_MODEL = "gpt-5.6-terra"
MAX_CONTEXT_CHARS = int(os.getenv("GENEALOGY_MAX_CONTEXT_CHARS", "140000"))

CONTEXT_FILES = [
    "PROMPT_MAESTRO.md",
    "familias/README.md",
    "familias/valderrama-ordonez.md",
    "familias/mutis.md",
    "familias/martinez-cabrales.md",
    "familias/pino-bechara.md",
    "familias/farah-mizrahy.md",
    "familias/fajardo-valderrama.md",
    "familias/conexiones-literarias.md",
    "fuentes/README.md",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def build_context() -> str:
    chunks: list[str] = []
    used = 0
    for rel in CONTEXT_FILES:
        text = read_text(ROOT / rel)
        if not text:
            continue
        block = f"\n\n===== ARCHIVO: {rel} =====\n{text}"
        if used + len(block) > MAX_CONTEXT_CHARS:
            remaining = MAX_CONTEXT_CHARS - used
            if remaining > 500:
                chunks.append(block[:remaining] + "\n[CONTEXTO TRUNCADO POR LÍMITE]\n")
            break
        chunks.append(block)
        used += len(block)
    return "".join(chunks)


def run_git(args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return f"[git {' '.join(args)} falló: {proc.stderr.strip()}]"
    return proc.stdout


def build_manual_diff(before: str | None, after: str | None) -> str:
    tracked = [
        "aportes-manuales",
        "familias",
        "PROMPT_MAESTRO.md",
        "entrevistas",
        "fuentes",
    ]
    if before and after and not re.fullmatch(r"0+", before):
        return run_git(["diff", "--unified=5", before, after, "--", *tracked])
    if after:
        return run_git(["show", "--format=fuller", "--stat", "--patch", after, "--", *tracked])
    return run_git(["diff", "--unified=5", "HEAD~1", "HEAD", "--", *tracked])


def load_queue() -> list[dict[str, str]]:
    data = json.loads(read_text(AGENT_DIR / "research_queue.json"))
    topics = data.get("topics", [])
    if not isinstance(topics, list) or not topics:
        raise RuntimeError("research_queue.json no contiene temas")
    return topics


def choose_topic(explicit: str | None) -> dict[str, str]:
    topics = load_queue()
    if explicit:
        for topic in topics:
            if topic.get("id") == explicit:
                return topic
        raise RuntimeError(f"Tema desconocido: {explicit}")
    index = datetime.now(timezone.utc).toordinal() % len(topics)
    return topics[index]


def recursive_objects(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from recursive_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from recursive_objects(child)


def extract_sources(response: Any) -> list[dict[str, str]]:
    try:
        raw = response.model_dump()
    except Exception:
        return []
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for obj in recursive_objects(raw):
        url = obj.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        if url in seen:
            continue
        seen.add(url)
        title = obj.get("title") or obj.get("name") or "Fuente web"
        sources.append({"title": str(title), "url": url})
    return sources


def is_insufficient_quota_error(exc: Exception) -> bool:
    """Detecta únicamente ausencia de saldo/créditos, no otros 429 transitorios."""
    text = str(exc).lower()
    markers = (
        "insufficient_quota",
        "credit_balance_exhausted",
        "no credits remaining",
        "add credits to continue using the api",
    )
    return any(marker in text for marker in markers)


def call_agent(task: str, context: str) -> tuple[str, list[dict[str, str]], str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Configure el secreto del repositorio antes de ejecutar el agente."
        )

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    client = OpenAI(api_key=api_key)
    system_prompt = read_text(AGENT_DIR / "SYSTEM_PROMPT.md")

    user_input = f"""
TAREA DE ESTA EJECUCIÓN
======================
{task}

CORPUS ACTUAL DEL REPOSITORIO
=============================
{context}

INSTRUCCIONES DE EJECUCIÓN
==========================
- Investiga activamente en la web y contrasta varias fuentes cuando sea posible.
- No presentes como nuevo lo que ya conste en el corpus.
- Busca evidencia que pueda falsar las hipótesis, no solo confirmarlas.
- Señala explícitamente si dos sitios parecen copiar la misma fuente.
- Mantén separados dato familiar, documento primario, fuente secundaria e inferencia.
- Si no puedes resolver un punto, dilo y especifica el documento exacto que falta.
- Produce el informe en español y respeta exactamente la estructura exigida por el prompt del sistema.
"""

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_input,
        tools=[{"type": "web_search"}],
        include=["web_search_call.action.sources"],
        store=False,
    )
    text = (response.output_text or "").strip()
    if not text:
        text = "El modelo no devolvió texto de informe. Revisar el objeto de respuesta/API."
    return text, extract_sources(response), model


def source_appendix(sources: list[dict[str, str]]) -> str:
    if not sources:
        return "\n\n## Fuentes recuperadas por la herramienta de búsqueda\n\nNo se recuperaron URLs estructuradas en esta ejecución.\n"
    lines = ["\n\n## Fuentes recuperadas por la herramienta de búsqueda\n"]
    for src in sources:
        title = src["title"].replace("\n", " ").strip()
        lines.append(f"- [{title}]({src['url']})")
    return "\n".join(lines) + "\n"


def write_report(kind: str, slug: str, task: str, body: str, sources: list[dict[str, str]], model: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H-%M-%SZ")
    safe_slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-")[:80] or "general"
    path = REPORTS_DIR / f"{stamp}__{kind}__{safe_slug}.md"
    header = f"""# Informe automático del Agente Genealógico

- **Ejecución UTC:** {now.isoformat()}
- **Modo:** `{kind}`
- **Tema:** `{slug}`
- **Modelo:** `{model}`
- **Estado:** propuesta para revisión humana; no modifica por sí sola el árbol canónico.

## Tarea

{task}

---

"""
    path.write_text(header + body + source_appendix(sources), encoding="utf-8")
    return path


def do_research(topic_id: str | None, context: str) -> Path:
    topic = choose_topic(topic_id)
    task = (
        f"Ronda autónoma de investigación. Tema: {topic['title']}.\n\n"
        f"Objetivo específico: {topic['query']}"
    )
    body, sources, model = call_agent(task, context)
    return write_report("research", topic["id"], task, body, sources, model)


def do_validation(before: str | None, after: str | None, context: str) -> Path | None:
    diff = build_manual_diff(before, after).strip()
    if not diff:
        print("No hay cambios relevantes que validar.")
        return None
    if len(diff) > 100000:
        diff = diff[:100000] + "\n[DIFF TRUNCADO]\n"
    task = f"""Audita los siguientes cambios o aportes manuales.

Para CADA afirmación nueva o modificada:
1. extráela de forma atómica;
2. compárala contra el corpus existente;
3. investiga en la web evidencia a favor y en contra;
4. identifica posibles homónimos o inconsistencias cronológicas;
5. asigna A/B/C/D/E/X;
6. recomienda aceptar, corregir, mantener como tradición oral o rechazar;
7. especifica qué archivo canónico debería cambiar, pero NO lo modifiques.

DIFF / APORTE:
```diff
{diff}
```
"""
    body, sources, model = call_agent(task, context)
    return write_report("validation", "manual-input", task, body, sources, model)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agente genealógico auditable")
    parser.add_argument("--mode", choices=["research", "validate", "full"], default=os.getenv("AGENT_MODE", "research"))
    parser.add_argument("--topic", default=os.getenv("AGENT_TOPIC") or None)
    parser.add_argument("--before", default=os.getenv("GIT_BEFORE") or None)
    parser.add_argument("--after", default=os.getenv("GIT_AFTER") or None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context = build_context()
    outputs: list[Path] = []
    try:
        if args.mode in {"validate", "full"}:
            report = do_validation(args.before, args.after, context)
            if report:
                outputs.append(report)
        if args.mode in {"research", "full"}:
            outputs.append(do_research(args.topic, context))
    except Exception as exc:
        if is_insufficient_quota_error(exc):
            print(
                "::warning::Agente genealógico omitido: la API de OpenAI no tiene créditos disponibles. "
                "El workflow queda en estado correcto y volverá a investigar automáticamente cuando se habilite billing.",
                file=sys.stderr,
            )
            return 0
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for output in outputs:
        print(f"REPORT={output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
