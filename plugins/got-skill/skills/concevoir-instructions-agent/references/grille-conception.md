# Grille de conception d'un agent

## Cadrage

- Quel résultat observable produire, pour qui et dans quel contexte ?
- Quelles entrées sont obligatoires, facultatives ou récupérables ?
- Qu'est-ce qui est hors périmètre ?

## Décisions et permissions

- Quelles règles métier modifient le résultat ?
- Quelles ambiguïtés exigent une question ?
- Quels cas imposent un arrêt, un avertissement ou une validation humaine ?
- Quel retour d'outil prouve la réussite et quel repli produire sans outil ?

## Qualité

- Faits, hypothèses et recommandations sont-ils distingués ?
- Les contraintes sont-elles testables ?
- Les répétitions et prescriptions sans justification ont-elles été retirées ?
- Les exemples sont-ils synthétiques et non confidentiels ?

## Moderniser un ancien prompt

Retirer les injonctions « réfléchis étape par étape », répétitions en majuscules, validations à chaque micro-étape et formats rigides sans valeur métier. Les remplacer par des critères de réussite, seuils de décision, sorties structurées et confirmations liées au risque réel.
