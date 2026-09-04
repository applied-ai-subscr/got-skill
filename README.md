# Got Skill

Marketplace communautaire de skills francophones issus de cas d'usage métier éprouvés, modernisés pour les agents actuels.

Le dépôt distribue chaque skill séparément ou dans un pack unique. Les skills utilisent le format `SKILL.md`, fonctionnent sans intégration propriétaire et peuvent employer des connecteurs MCP lorsqu'ils sont disponibles.

## Skills disponibles

- `rediger-annonce-emploi` : transforme une fiche de poste et une annonce modèle en annonce cohérente.
- `gerer-backoffice-crm` : extrait, vérifie et prépare des données d'entreprise pour un CRM ou un contrat.
- `concevoir-instructions-agent` : crée ou améliore les instructions d'un assistant ou agent IA.
- `creer-sequence-prospection` : conçoit une séquence de prospection personnalisée.
- `evaluer-candidat` : mesure l'adéquation d'un candidat, prépare un entretien et produit une synthèse.

## Structure

```text
.claude-plugin/marketplace.json
plugins/got-skill/
  .claude-plugin/plugin.json
  skills/<nom-du-skill>/
    SKILL.md
    agents/openai.yaml
    references/*.md
scripts/validate_marketplace.py
```

Les exports GPT et leurs documents sources restent locaux et sont exclus de Git. Les connaissances utiles ont été reformulées dans des références Markdown neutres. Aucun PDF ou DOCX source n'est distribué.

## Validation

```bash
python3 scripts/validate_marketplace.py
```

## Installation

Dans une application compatible avec les marketplaces Claude, ajoutez l'URL du dépôt puis installez `got-skill`. Pour un agent compatible avec le format ouvert des skills, copiez le dossier du skill souhaité dans son répertoire de skills.

## Licence

Apache-2.0. Les marques, documents et contenus tiers ne sont pas inclus dans cette distribution.
