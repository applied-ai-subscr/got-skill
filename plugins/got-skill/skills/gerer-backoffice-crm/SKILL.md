---
name: gerer-backoffice-crm
description: Extraire, vérifier et rapprocher les informations d'une entreprise depuis un KBIS, un contrat ou un CRM, puis préparer une création CRM, une mise à jour ou un contrat. Utiliser pour les opérations back-office avec connecteurs MCP optionnels.
---

# Gérer les données back-office et CRM

Guider l'utilisateur depuis les documents sources jusqu'à une donnée structurée ou une action externe contrôlée.

## Cadrage

Déterminer l'entreprise de l'utilisateur, la contrepartie et l'objectif : vérifier les données, créer ou mettre à jour une fiche CRM, rapprocher plusieurs sources, ou préparer un contrat. Regrouper les demandes d'informations manquantes lorsque cela accélère le travail.

## Vérification

1. Extraire les identifiants et coordonnées depuis les documents fournis.
2. Attribuer à chaque valeur sa source et sa date lorsqu'elles sont connues.
3. Signaler les divergences entre KBIS, contrat, CRM et registre externe ; ne pas choisir silencieusement.
4. Pour une entreprise française, privilégier le SIREN et valider son format avant une recherche.
5. Mapper une liste fermée uniquement lorsque la correspondance est certaine et rendre l'association visible.

Lire [references/modele-donnees.md](references/modele-donnees.md) pour les champs attendus et [references/integrations-mcp.md](references/integrations-mcp.md) avant un connecteur.

## Actions externes

Utiliser les outils MCP disponibles pour le registre d'entreprises, le CRM, le stockage ou les documents. Toute création, mise à jour ou envoi nécessite un récapitulatif et l'accord explicite de l'utilisateur juste avant l'action.

Si le connecteur manque, produire une charge utile structurée ou un fichier d'import. Ne jamais inventer un identifiant, écraser une divergence ou affirmer qu'une action a réussi sans retour de l'outil.
