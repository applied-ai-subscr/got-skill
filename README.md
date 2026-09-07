# Got Skill

Marketplace communautaire de skills francophones, issus d'anciens GPTs personnalisés éprouvés en entreprise et portés au format ouvert `SKILL.md`. Chaque skill conserve la logique d'origine du GPT (parcours guidé, portes d'entrée, gabarits, ton, exemples) ; seules les mécaniques propriétaires ont été modernisées (actions Zapier remplacées par des connecteurs MCP décrits par capacité).

## Skills disponibles

| Skill | GPT d'origine | Ce qu'il fait |
|---|---|---|
| `rediger-annonce-emploi` | L'Annonce Magique | Annonce standardisée à partir d'une fiche de poste ET d'une annonce modèle de l'entreprise |
| `gerer-backoffice-crm` | Assistant Back-Office CRM | Création ou mise à jour d'une entreprise dans le CRM depuis un KBIS, vérification Pappers, préparation de contrat |
| `concevoir-instructions-agent` | Meta Prompt | Création ou optimisation des instructions d'un assistant à partir d'un processus métier ou d'instructions existantes |
| `creer-sequence-prospection` | Sequence Prospection Magic | Séquence de cold emails pour Lemlist, HubSpot ou Mixmax via une découverte guidée |
| `evaluer-candidat` | Talent Alchimie | Analyse d'adéquation candidat / appel d'offres, questions d'entretien ou fiche synthèse |

## Installation

**Claude Code**

```
/plugin marketplace add applied-ai-subscr/got-skill
/plugin install got-skill@got-skill-marketplace
```

**Codex / ChatGPT desktop**

```
codex plugin marketplace add applied-ai-subscr/got-skill
```

puis installer « Got Skill » depuis le répertoire des plugins.

**Hermes Agent et autres agents compatibles `SKILL.md`**

Télécharger l'archive `<nom-du-skill>.skill` d'une release GitHub et la décompresser dans le répertoire des skills de l'agent (par exemple `~/.hermes/skills/`). L'installation par URL directe ne récupère que `SKILL.md` et oublie le dossier `references/` : préférer l'archive.

## Structure

```text
.claude-plugin/marketplace.json        # marketplace Claude Code
.agents/plugins/marketplace.json       # marketplace Codex
plugins/got-skill/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  skills/<nom-du-skill>/
    SKILL.md                           # parcours complet du skill
    agents/openai.yaml                 # métadonnées Codex
    references/*.md                    # gabarits, exemples, repères
scripts/validate_marketplace.py
```

## Connecteurs MCP

Les skills fonctionnent sans intégration. Quand un connecteur MCP est disponible (registre d'entreprises Pappers, CRM HubSpot, documents), ils l'utilisent en lecture et demandent toujours une confirmation explicite avant toute écriture.

## Tests

Chaque skill embarque ses scénarios de test dans `evals/` (`evals.json` et documents d'entrée synthétiques). Les scénarios ont été rejoués en dialogue simulé face aux instructions d'origine du GPT, puis face au skill, avec des critères de fidélité : ordre des étapes, messages imposés, gabarits. Méthode, protocole et résultats : [plugins/got-skill/evals/README.md](plugins/got-skill/evals/README.md).

Les exports GPT et les documents sources restent locaux et ne sont pas distribués.

## Validation

```bash
python3 scripts/validate_marketplace.py   # structure du marketplace (CI)
python3 scripts/run_evals.py validate     # structure des évals, hors-ligne (CI)

# Rejeu conversationnel de fidélité (nécessite un endpoint OpenAI-compatible) :
#   GOTSKILL_EVAL_API_KEY=... python3 scripts/run_evals.py replay [skill]
# Agrégation des résultats de runs en gate (code non nul si une assertion échoue) :
python3 scripts/run_evals.py grade --out eval-workspace/runs
```

## Licence

Apache-2.0. Les marques, documents et contenus tiers ne sont pas inclus dans cette distribution.
