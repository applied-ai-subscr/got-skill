#!/usr/bin/env python3
"""Run and gate the got-skill fidelity evals.

Stdlib-only (matching validate_marketplace.py). Three concerns:

  validate (default)   Structural checks on every skill's evals/evals.json:
                       expected fields, referenced files present, non-empty
                       expectations. Fully offline -> safe for CI. Exits 1 on
                       any structural error. This is the deterministic "green"
                       gate enforced by the repository.

  list                 Print the discovered evals / skills.

  replay [skill]       Conversational fidelity replay, credential-gated.
                       An assistant (following SKILL.md) plays against a
                       scripted user (dossier_utilisateur). Writes, under
                       --out/<skill>/run-<stamp>/, conversation.md,
                       expected_output files and grading.json (one entry per
                       expectation + summary). Requires an OpenAI-compatible
                       endpoint via env:
                         GOTSKILL_EVAL_API_BASE  (default http://localhost:8000/v1)
                         GOTSKILL_EVAL_MODEL     (default deepseek-ai/DeepSeek-V4-Flash-0731)
                         GOTSKILL_EVAL_API_KEY   (optional key)
                       Each eval is capped at --max-turns (default 12) user
                       turns, as in the documented protocol.

  grade [--out DIR]    Aggregate every grading.json found under --out and report
                       pass/fail/total per skill, exit non-zero if any assertion
                       failed OR if any run lacks a grading.json.

Examples
  python3 scripts/run_evals.py                 # validation only (CI)
  python3 scripts/run_evals.py list
  GOTSKILL_EVAL_API_KEY=... python3 scripts/run_evals.py replay evaluer-candidat
  python3 scripts/run_evals.py grade --out eval-workspace/runs
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "got-skill"
SKILLS = PLUGIN / "skills"

REQUIRED_EVAL_FIELDS = ("id", "prompt", "expected_output", "expectations")
REQUIRED_USER_FIELD = "dossier_utilisateur"
DEFAULT_OUT = ROOT / "eval-workspace" / "runs"


def _resolve(path: Path) -> Path:
    return path.expanduser().resolve()


# --------------------------------------------------------------------------- #
# Discovery & structural validation
# --------------------------------------------------------------------------- #
def discover_evals() -> list[tuple[Path, dict, list[dict]]]:
    """Return (skill_dir, evals_json, evals_list) for every skill with an eval."""
    out: list[tuple[Path, dict, list[dict]]] = []
    if not SKILLS.is_dir():
        return out
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        evals_file = skill_dir / "evals" / "evals.json"
        if not evals_file.is_file():
            continue
        try:
            data = json.loads(evals_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            data = {"_broken": str(exc)}
        raw_evals = data.get("evals") if isinstance(data, dict) else None
        evals_list = [e for e in raw_evals if isinstance(e, dict)] if isinstance(raw_evals, list) else []
        out.append((skill_dir, data, evals_list))
    return out


def validate(verbose: bool = True) -> int:
    errors: list[str] = []
    discovered = discover_evals()
    if not discovered:
        errors.append("No skill evals found under " + PLUGIN.as_posix())
    for skill_dir, data, evals_list in discovered:
        rel = skill_dir.name
        evals_file = skill_dir / "evals" / "evals.json"
        if "_broken" in data:
            errors.append(f"{rel}: evals.json is not valid JSON: {data['_broken']}")
            continue
        if data.get("skill_name") != rel:
            errors.append(f"{rel}: skill_name {data.get('skill_name')!r} != dir {rel!r}")
        if not isinstance(evals_list, list) or not evals_list:
            errors.append(f"{rel}: 'evals' must be a non-empty list")
            continue
        files_dir = skill_dir / "evals" / "files"
        for ev in evals_list:
            label = f"{rel}/eval-{ev.get('id', '?')}"
            for field in REQUIRED_EVAL_FIELDS:
                if field not in ev:
                    errors.append(f"{label}: missing field '{field}'")
            for field in (REQUIRED_USER_FIELD,):
                if field not in ev:
                    errors.append(f"{label}: missing field '{field}'")
            exps = ev.get("expectations")
            if not isinstance(exps, list) or not exps:
                errors.append(f"{label}: 'expectations' must be a non-empty list")
            for i, e in enumerate(exps or []):
                if not isinstance(e, str) or not e.strip():
                    errors.append(f"{label}: expectation {i} empty/not a string")
            for f in ev.get("files", []) or []:
                if not (files_dir / f).is_file():
                    errors.append(f"{label}: referenced file missing: files/{f}")
    if verbose:
        total = sum(len(el) for _, _, el in discovered)
        print(f"Evals: {len(discovered)} skills, {total} scenarios")
    if errors:
        print("Eval validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Eval validation OK")
    return 0


def list_evals() -> int:
    discovered = discover_evals()
    if not discovered:
        print("No evals found.")
        return 0
    print(f"{'SKILL':<28}{'$':>6}  scenarios")
    for skill_dir, _, evals_list in discovered:
        n = sum(len(e.get("expectations", [])) for e in evals_list)
        print(f"{skill_dir.name:<28}{n:>6}  {len(evals_list)}")
    return 0


# --------------------------------------------------------------------------- #
# Grading aggregation (offline green gate over produced grading files)
# --------------------------------------------------------------------------- #
def grade(out: Path) -> int:
    if not out.is_dir():
        print(f"No run directory: {out}")
        return 1
    gradings = sorted(out.glob("*/run-*/grading.json"))
    by_skill: dict[str, list[dict]] = {}
    missing: list[str] = []
    for skill_dir in sorted(p for p in out.iterdir() if p.is_dir()):
        runs = sorted(skill_dir.glob("run-*/grading.json"))
        if not runs:
            missing.append(skill_dir.name)
    for g in gradings:
        skill = g.parts[-3]
        by_skill.setdefault(skill, []).append(json.loads(g.read_text(encoding="utf-8")))
    if not gradings and not missing:
        print(f"No grading results under {out}")
        return 1
    total_p = total_f = total_t = 0
    print(f"{'SKILL':<28}{'ok':>4}{'ko':>4}{'tot':>5}  taux")
    for skill in sorted(by_skill):
        p = sum(x["summary"]["passed"] for x in by_skill[skill])
        f = sum(x["summary"]["failed"] for x in by_skill[skill])
        t = p + f
        total_p += p; total_f += f; total_t += t
        print(f"{skill:<28}{p:>4}{f:>4}{t:>5}  {p/t:.0%}" if t else f"{skill:<28}{p:>4}{f:>4}{t:>5}")
    if missing:
        print("Runs without grading.json:")
        for m in missing:
            print(f"  - {m}")
    print("-" * 50)
    if total_t == 0:
        print("No graded assertions found.")
        return 1
    print(f"TOTAL{'':<23}{total_p:>4}{total_f:>4}{total_t:>5}  {total_p/total_t:.0%}")
    return 0 if (total_f == 0 and not missing) else 1


# --------------------------------------------------------------------------- #
# LLM plumbing (OpenAI-compatible)
# --------------------------------------------------------------------------- #
def llm_chat(base: str, model: str, api_key: str, messages: list[dict],
             temperature: float = 0.2, max_tokens: int | None = None) -> str:
    url = base.rstrip("/") + "/chat/completions"
    payload: dict = {"model": model, "messages": messages, "temperature": temperature}
    if max_tokens:
        payload["max_tokens"] = max_tokens
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {api_key}"} if api_key else {})},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"]


def _system_skill_text(skill_dir: Path, ev: dict) -> str:
    parts = ["Tu es un assistant qui applique STRICTEMENT le skill ci-dessous.",
             "=== SKILL.md ===", (skill_dir / "SKILL.md").read_text(encoding="utf-8")]
    refs = sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").is_dir() else []
    for r in refs:
        parts.append(f"\n=== reference: {r.name} ===\n{r.read_text(encoding='utf-8')}")
    return "\n".join(parts)


def _system_user_text(ev: dict) -> str:
    return (
        "Tu joues le rôle de l'UTILISATEUR dans un dialogue d'évaluation.\n"
        "Réponds uniquement à partir de ce dossier de rôle, sinon par « je ne sais pas ».\n"
        "Ne rédige jamais le texte de l'assistant : tu es l'utilisateur.\n"
        f"Dossier utilisateur : {ev.get('dossier_utilisateur', '(aucune consigne)')}"
    )


def _save_outputs(run_dir: Path, expected_output: str, final_assistant: str) -> list[str]:
    """Best-effort extraction of requested deliverable files from the final turn."""
    saved: list[str] = []
    names = [n.strip() for n in expected_output.replace("et", ",").split(",") if n.strip()]
    for name in names:
        if not name.endswith((".md", ".json", ".csv")):
            name = name + ".md"
        # try fenced block for that file name
        fenced = _extract_fenced(final_assistant, name)
        (run_dir / name).write_text(fenced or final_assistant, encoding="utf-8")
        saved.append(name)
    return saved


def _extract_fenced(text: str, fname: str) -> str | None:
    import re
    # ```filename or ```lang ... ``` blocks
    blocks = re.findall(r"```[^\n]*?{0}[^\n]*\n(.*?)```".format(re.escape(fname)), text, flags=re.DOTALL)
    if blocks:
        return blocks[0]
    blocks = re.findall(r"```[a-z]*\n(.*?)```", text, flags=re.DOTALL)
    return blocks[0] if len(blocks) == 1 else None


# --------------------------------------------------------------------------- #
# Replay (credential-gated)
# --------------------------------------------------------------------------- #
def replay(skill_filter: str | None, out: Path, base: str, model: str,
           api_key: str, max_turns: int) -> int:
    discovered = discover_evals()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    ran = 0
    for skill_dir, data, evals_list in discovered:
        if skill_filter and skill_dir.name != skill_filter:
            continue
        for ev in evals_list:
            run_dir = out / skill_dir.name / f"run-{stamp}-eval{ev.get('id')}"
            run_dir.mkdir(parents=True, exist_ok=True)
            conv: list[dict] = [{"role": "user", "content": ev["prompt"]}]
            transcript: list[str] = [f"# Conversation — {skill_dir.name} / eval-{ev.get('id')}"]
            user_turns = 0
            final_assistant = ""
            while user_turns < max_turns:
                asst = llm_chat(base, model, api_key,
                                [{"role": "system", "content": _system_skill_text(skill_dir, ev)}] + conv)
                conv.append({"role": "assistant", "content": asst})
                transcript.append(f"\n## Tour — Assistant\n{asst}")
                final_assistant = asst
                deliverable_names = [n.strip() for n in ev["expected_output"].split(",")]
                if any(n in asst for n in deliverable_names if n):
                    break  # assistant signalled it produced the deliverable
                user_turns += 1
                usr = llm_chat(base, model, api_key,
                               [{"role": "system", "content": _system_user_text(ev)}] + conv)
                conv.append({"role": "user", "content": usr})
                transcript.append(f"\n## Tour — Utilisateur\n{usr}")
            (run_dir / "conversation.md").write_text("\n".join(transcript), encoding="utf-8")
            saved = _save_outputs(run_dir, ev["expected_output"], final_assistant)
            grading = _grade_via_llm(base, model, api_key, skill_dir, ev, transcript, saved)
            (run_dir / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"eval-{ev.get('id')} {skill_dir.name}: outputs={saved} -> {run_dir.relative_to(ROOT)}")
            ran += 1
    if ran == 0:
        print("No evals replayed.")
        return 1
    print(f"Replayed {ran} eval(s). Runs in {out.relative_to(ROOT)}")
    return 0


def _grade_via_llm(base, model, api_key, skill_dir, ev, transcript, saved) -> dict:
    exps = ev["expectations"]
    prompt = (
        "Voici la transcription d'un dialogue où un assistant applique un skill métier.\n\n"
        f"TRANSCRIPT:\n{' '.join(transcript)}\n"
        "Fichiers livrés dans le répertoire de run (le cas échéant) : "
        + (", ".join(saved) if saved else "aucun") + ".\n\n"
        "Évalue chacune des assertions suivantes à partir de la transcription. "
        "Réponds UNIQUEMENT en JSON : {\"expectations\":[{\"text\":\"...\",\"passed\":true/false,\"evidence\":\"...\"}]}.\n"
        "Assertions:\n" + "\n".join(f"- {i+1}. {e}" for i, e in enumerate(exps))
    )
    try:
        raw = llm_chat(base, model, api_key,
                       [{"role": "user", "content": prompt}], temperature=0.0, max_tokens=3000)
        raw = raw[raw.find("{"):raw.rfind("}") + 1]
        results = json.loads(raw)["expectations"]
    except Exception:
        results = [{"text": e, "passed": False,
                    "evidence": "grading LLM unavailable; run 'grade' gates only on real runs"}
                   for e in exps]
    if len(results) != len(exps):
        results = [{"text": e, "passed": False, "evidence": "grading parse mismatch"} for e in exps]
    passed = sum(1 for r in results if r.get("passed"))
    return {
        "expectations": results,
        "summary": {"passed": passed, "failed": len(results) - passed,
                    "total": len(results), "pass_rate": passed / len(results)},
    }


# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="run_evals.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("validate", help="structural checks (default, CI-safe)")
    sub.add_parser("list", help="list evals")
    g = sub.add_parser("grade", help="aggregate grading.json and gate")
    g.add_argument("--out", type=Path, default=DEFAULT_OUT)
    r = sub.add_parser("replay", help="LLM conversational replay (credential-gated)")
    r.add_argument("skill", nargs="?", help="skill name filter")
    r.add_argument("--out", type=Path, default=DEFAULT_OUT)
    r.add_argument("--max-turns", type=int, default=12)
    r.add_argument("--api-base", default=os.environ.get("GOTSKILL_EVAL_API_BASE", "http://localhost:8000/v1"))
    r.add_argument("--model", default=os.environ.get("GOTSKILL_EVAL_MODEL", "deepseek-ai/DeepSeek-V4-Flash-0731"))
    r.add_argument("--api-key", default=os.environ.get("GOTSKILL_EVAL_API_KEY", ""))

    args = ap.parse_args(argv)
    cmd = args.cmd or "validate"
    if cmd == "validate":
        return validate()
    if cmd == "list":
        return list_evals()
    if cmd == "grade":
        return grade(_resolve(args.out))
    if cmd == "replay":
        if not args.api_key and not os.environ.get("GOTSKILL_EVAL_API_KEY"):
            print("replay needs an API key (GOTSKILL_EVAL_API_KEY) or use --api-key.")
            return 1
        return replay(args.skill, _resolve(args.out), args.api_base, args.model, args.api_key, args.max_turns)
    ap.error(f"unknown command {cmd!r}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
