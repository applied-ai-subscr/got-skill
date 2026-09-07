# Consignes pour les agents

## Périmètre

Ce dépôt distribue des skills métier issus d'anciens GPTs personnalisés. La priorité est la fidélité à la logique d'origine de chaque GPT : parcours, portes d'entrée, gabarits, ton, exemples. La concision vient ensuite : les gabarits et exemples vont dans `references/`, le corps du `SKILL.md` garde le parcours complet.

## Modernisation autorisée

- Remplacer les actions Zapier par des outils MCP décrits par capacité, avec repli sans connecteur.
- Retirer le boilerplate « Chain of Thought / ReAct » sans retirer les étapes métier.
- Ne pas redemander une information déjà fournie ; garder l'ordre des étapes.

## Confidentialité

- Ne jamais versionner les exports XML, PDF ou DOCX sources (`/*.xml`, `/talent-alchimie/`, `/sequence-prospection-magic/`, `/eval-workspace/`).
- Ne jamais ajouter de référence à l'ancien employeur, ni de logo, donnée, exemple ou modèle issu de cette entreprise.
- Les références distribuées sont en Markdown et réécrites de manière générique ; les exemples sont synthétiques.

## Structure

- Chaque dossier sous `plugins/got-skill/skills/` contient un `SKILL.md`, un `agents/openai.yaml` (Codex) et des `references/*.md`.
- Les évals de fidélité vivent dans `eval-workspace/evals/<skill>.json` (local) ; les scénarios sont conversationnels (dossier utilisateur scripté).

## Livraison

Exécuter `python3 scripts/validate_marketplace.py` avant toute publication. Une publication GitHub ou un push nécessite une demande explicite de l'utilisateur.
