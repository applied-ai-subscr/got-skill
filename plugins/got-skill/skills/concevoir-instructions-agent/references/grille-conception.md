# Grille d'audit d'instructions existantes

## Points forts à conserver
- Parcours et ordre des étapes, portes d'entrée (documents obligatoires, messages imposés).
- Règles métier chiffrées : seuils, plafonds, délais, refus.
- Ton, langue, formats de sortie et exemples.

## Faiblesses fréquentes
- Règles métier détachées du flux : préciser à quelle étape chaque règle s'applique.
- Incohérence entre l'objectif d'une étape et l'action demandée.
- Cas limites absents : entrée incomplète ou illisible, plusieurs documents d'un coup, fin de collecte, hors sujet.
- Action externe sans récapitulatif ni validation globale.
- Mécaniques propriétaires obsolètes (Zapier, `list_available_actions`, `run_action`) : remplacer par une description par capacité avec repli sans outil.
- Injonctions génériques (« réfléchis étape par étape », majuscules impératives, `####`) : remplacer par des critères de réussite observables.
- Aucun exemple de conversation.

## Questions de cadrage
- Quel résultat observable produire, pour qui, dans quel contexte ?
- Quelles entrées sont obligatoires, facultatives ou récupérables par un outil ?
- Quelles ambiguïtés exigent une question ? Quels cas imposent un arrêt ou une validation humaine ?
- Quel retour d'outil prouve la réussite ?
- Les exemples sont-ils synthétiques et non confidentiels ?
