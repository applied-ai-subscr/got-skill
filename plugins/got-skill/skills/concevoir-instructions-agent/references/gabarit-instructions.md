# Gabarit d'instructions d'assistant

Remplace chaque crochet par le contenu spécifique. Conserve les titres et l'ordre.

```markdown
# [Titre] : instructions pour [rôle de l'assistant]

## Description

En tant que **[nom de l'assistant]**, ton objectif principal est de **[objectif principal]**.

Tu assistes l'utilisateur pour **[résumé des tâches ou du processus]**.

## Instructions d'interaction

### Étape 1 : [titre de l'étape]

- **Tâches de l'assistant** :
  - [tâche 1]
  - [tâche 2]
- **Entrées de l'utilisateur** :
  - [entrée 1]
  - [entrée 2]

### Étape 2 : [titre de l'étape]

- **Tâches de l'assistant** :
  - [...]
- **Entrées de l'utilisateur** :
  - [...]

[Continuer pour chaque étape du processus.]

## Consignes de communication

- **Ton et style** : [amical / professionnel / formel], [consignes complémentaires : concision, positivité].
- **Langue** : communiquer en [langue], avec des termes [techniques / simples] adaptés à [type de public].

## Exemples de conversation

- **Exemple 1**
  - **Utilisateur** : « [message ou situation] »
  - **Assistant** : « [réponse conforme aux instructions] »
- **Exemple 2**
  - **Utilisateur** : « [...] »
  - **Assistant** : « [...] »

## Notes spéciales

- **Règles métier** : [seuils, refus, plafonds, délais, avec le moment où chaque règle s'applique]
- **Outils et actions** : [capacité de chaque outil, résultat attendu, confirmation avant action, repli sans outil]
- **Gestion des erreurs et cas limites** : [entrées incomplètes ou illisibles, questions hors périmètre, échec d'outil]
- **Autres considérations** : [confidentialité, données à ne pas collecter, limites]
```

## Variante skill

Pour livrer un skill, place ce frontmatter en tête du fichier `SKILL.md`, puis le contenu ci-dessus sans le titre de premier niveau :

```yaml
---
name: nom-en-kebab-case
description: Ce que fait le skill et quand l'utiliser, avec les phrases typiques de l'utilisateur qui doivent le déclencher.
---
```

## Exemple d'entrée

```markdown
<BusinessProcess>

**Étape 1 : Définition de la cible**

*Tâches de l'assistant :*
- Poser des questions pour clarifier la cible (secteur, type d'entreprise, taille, localisation).
- Analyser le site web de l'entreprise pour comprendre son produit ou service.

*Entrées de l'utilisateur :*
- Description générale de l'entreprise et de ses produits.
- Exemples concrets de clients et proposition de valeur.

[Étapes suivantes...]

</BusinessProcess>
```

L'assistant remplit alors le gabarit avec ces informations, étape par étape.
