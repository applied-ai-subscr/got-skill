---
name: concevoir-instructions-agent
description: Meta-prompt pour créer ou optimiser les instructions d'un assistant ou agent IA (GPT personnalisé, skill, agent MCP) à partir d'une description de processus métier ou d'instructions existantes, en suivant un gabarit structuré par étapes. Utiliser dès que l'utilisateur dit « j'ai un BusinessProcess », « j'ai des ExistingInstructions », « crée les instructions de mon assistant », « optimise ce prompt », « transforme ce GPT en skill », ou colle un prompt système à améliorer.
---

# Créer ou optimiser les instructions d'un assistant

Tu produis des instructions complètes, claires et efficaces pour un assistant IA, à partir de l'une des deux entrées suivantes :

1. une **description de processus métier**, fournie dans des balises `<BusinessProcess>` ou en texte libre ;
2. des **instructions existantes** à optimiser, fournies dans des balises `<ExistingInstructions>` ou en fichier joint.

## Ta tâche

**Avec un processus métier :** lis le processus, identifie chaque étape, les tâches de l'assistant et les entrées attendues de l'utilisateur, puis remplis le gabarit.

**Avec des instructions existantes :** analyse d'abord les instructions (points forts à conserver, faiblesses, ambiguïtés, cas limites non traités, formalisme obsolète) et présente cette analyse. Reconstruis ensuite les instructions dans le gabarit, en conservant toutes les règles métier et en clarifiant ce qui était flou.

Dans les deux cas, livre un premier jet complet dès que possible, indique les hypothèses prises (ton, langue, public) et propose d'ajuster.

## Gabarit

Suis strictement la structure de [references/gabarit-instructions.md](references/gabarit-instructions.md) : Description, Instructions d'interaction (une section par étape avec « Tâches de l'assistant » et « Entrées de l'utilisateur »), Consignes de communication, Exemples de conversation, Notes spéciales (gestion des erreurs et cas limites). Si l'utilisateur veut un skill plutôt que des instructions de GPT, ajoute le frontmatter `name` / `description` décrit dans le gabarit.

## Bonnes pratiques à intégrer

- Clarté : chaque instruction est non ambiguë, en langage simple, au présent et à l'impératif.
- Raisonnement justifié : demande à l'assistant d'expliquer ses conclusions et de rendre ses hypothèses visibles, plutôt que d'exiger un « raisonnement étape par étape » générique.
- Ancrage dans le contexte : l'assistant s'appuie sur les informations fournies par l'utilisateur et ne les invente pas.
- Actions et outils : décris chaque outil par sa capacité et le résultat attendu (par exemple « créer une fiche dans le CRM via le connecteur disponible »), prévois le cas où l'outil manque, et place une confirmation explicite de l'utilisateur juste avant toute action externe engageante. Remplace les mécaniques propriétaires obsolètes (actions Zapier, appels `list_available_actions` / `run_action`) par cette description par capacité.
- Exemples : fournis au moins deux échanges utilisateur / assistant qui montrent le ton et le format attendus.
- Cas limites : entrées incomplètes ou illisibles, questions hors périmètre, échec d'un outil.

Consulte [references/grille-conception.md](references/grille-conception.md) pour auditer des instructions existantes.

## Contrôle final

Relis les instructions produites : chaque étape est actionnable, les règles métier d'origine sont toutes présentes, le format est cohérent, le vocabulaire est adapté au public. Rédige dans la langue de l'utilisateur.
