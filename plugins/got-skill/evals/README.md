# Évals de fidélité

Chaque skill embarque ses tests dans `skills/<skill>/evals/` :

- `evals.json` : les scénarios, au format `skill-creator` (`prompt`, `files`, `expected_output`, `expectations`), avec un champ supplémentaire `dossier_utilisateur` qui décrit l'utilisateur simulé et ce qu'il peut répondre.
- `files/` : les documents d'entrée. Tout est synthétique : sociétés, personnes, identifiants et domaines (`.example`) sont inventés.

Ces dossiers sont exclus des archives de release et n'alourdissent pas les installations.

## Méthode

Les skills sont issus de GPTs personnalisés. Pour vérifier que la migration n'a rien perdu, chaque scénario a d'abord été rejoué contre les instructions d'origine, puis contre le SKILL.md :

1. Rejouer les instructions initiales telles quelles sur les scénarios et observer le comportement (ordre des questions, messages imposés, gabarits, ton).
2. En déduire les assertions de fidélité (`expectations`).
3. Migrer les instructions dans `SKILL.md` et `references/`.
4. Rejouer les mêmes scénarios avec le skill et comparer.

Seules deux modernisations sont attendues et font échouer l'original : les Actions Zapier sont remplacées par des connecteurs MCP décrits par capacité, et le boilerplate Chain of Thought / ReAct est retiré.

## Protocole de dialogue

Un agent joue les deux rôles en alternance :

- **L'assistant** applique le `SKILL.md` et ses `references/` tels quels, y compris le ton, l'ordre des étapes et les messages imposés. Sans connecteur branché, il décrit ce qu'il ferait et n'appelle aucun outil externe.
- **L'utilisateur** est joué à partir du `dossier_utilisateur`. Il ne répond qu'avec ce que le dossier permet, sinon « je ne sais pas ». Quand le dossier renvoie à un fichier de `files/`, il le transmet à ce tour.

Le dialogue commence par le `prompt`, alterne assistant et utilisateur sans fusionner les tours, et s'arrête quand le livrable est produit ou après 12 tours utilisateur. Livrables : `conversation.md` (dialogue complet), les fichiers de `expected_output`, et un `grading.json` avec une entrée par assertion et sa preuve.

## Résultats

| Skill | Scénarios | GPT d'origine | Skill (it. 2) | Skill (it. 3) |
|---|---|---|---|---|
| rediger-annonce-emploi | 2 | 11/11 | 11/11 | 12/12 |
| gerer-backoffice-crm | 2 | 13/14 | 14/14 | 14/14 |
| concevoir-instructions-agent | 2 | 10/12 | 12/12 | 12/12 |
| creer-sequence-prospection | 3 | 11/11 | 10/11 | 15/15 |
| evaluer-candidat | 2 | 14/15 | 15/15 | 15/15 |

Itération 2 : 10 scénarios, 63 assertions, un run par configuration. Les échecs de l'original sont les mentions Zapier et Chain of Thought. L'échec du skill était un chiffre non sourcé dans un email, corrigé depuis.

Itération 3 (2026-09-07) : 11 scénarios après ajout d'un cas de réécriture d'email, 68 assertions, 68 passées.

Un seul run par scénario : les résultats sont indicatifs, pas statistiques.
