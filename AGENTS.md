# Consignes pour les agents

## Périmètre

Ce dépôt distribue des skills métier. Garder les instructions concises, portables et indépendantes d'un fournisseur de modèle.

## Confidentialité

- Ne jamais versionner les exports XML, PDF ou DOCX sources.
- Ne jamais ajouter de référence à Finaxys, ni de logo, donnée, exemple ou modèle issu de cette entreprise.
- Les références distribuées doivent être en Markdown et réécrites de manière générique.
- Les jeux de test éventuels doivent être entièrement synthétiques.

## Structure

- Chaque dossier sous `plugins/got-skill/skills/` contient un `SKILL.md`.
- Les connaissances conditionnelles vont dans `references/*.md`.
- Ne créer un dossier `assets/` que pour un véritable fichier de sortie réutilisable, jamais pour une base de connaissances.
- Les intégrations externes sont optionnelles et passent par des outils MCP disponibles dans l'environnement.

## Livraison

Exécuter `python3 scripts/validate_marketplace.py` avant toute publication. Une publication GitHub ou un push nécessite une demande explicite de l'utilisateur.
