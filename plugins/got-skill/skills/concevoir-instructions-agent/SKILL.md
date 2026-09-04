---
name: concevoir-instructions-agent
description: Créer, restructurer ou simplifier les instructions d'un assistant ou agent IA à partir d'un processus métier, d'un ancien prompt ou de cas d'usage. Utiliser pour produire des consignes testables, pas pour exposer un raisonnement interne détaillé.
---

# Concevoir les instructions d'un agent

Transformer le besoin fourni en instructions courtes qui changent réellement le comportement de l'agent.

Identifier l'objectif, les utilisateurs, les entrées, les livrables, les décisions sensibles, les outils, les autorisations et les critères de réussite. Distinguer les exigences des exemples historiques. Lire [references/grille-conception.md](references/grille-conception.md) pour auditer un ancien prompt.

## Conception

- Décrire le résultat attendu avant le déroulé.
- Garder les règles communes dans le fichier principal et les détails conditionnels dans des références.
- Laisser de la latitude lorsque plusieurs méthodes sont correctes.
- Imposer une séquence uniquement lorsqu'une dépendance, un risque ou une autorisation le justifie.
- Placer la confirmation au plus près d'une action externe engageante.
- Décrire les outils par capacité et résultat ; remplacer les intégrations obsolètes par des capacités MCP.
- Ne pas demander de révéler une chaîne de pensée. Demander une réponse justifiée, des hypothèses visibles et des contrôles observables.
- Ajouter des exemples seulement lorsqu'ils lèvent une ambiguïté importante.

Pour un skill, inclure un frontmatter discriminant, un corps concis et seulement les références ou scripts nécessaires. Vérifier les permissions, données sensibles, échecs d'outils et critères de sortie.
