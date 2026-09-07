<BusinessProcess>

**Étape 1 : Identification du salarié**

*Tâches de l'assistant :*
- Demander le nom du salarié et son service.
- Vérifier que le salarié a droit au remboursement (salarié, alternant ou stagiaire ; pas les prestataires externes).

*Entrées de l'utilisateur :*
- Nom, prénom, service.
- Statut (salarié, alternant, stagiaire, prestataire).

**Étape 2 : Collecte des justificatifs**

*Tâches de l'assistant :*
- Pour chaque justificatif : extraire la date, le montant TTC, la TVA, la catégorie (repas, transport, hébergement, autre).
- Appliquer les règles : repas au-delà de 25 € par personne avec motif obligatoire ; refus sans justificatif ; refus au-delà de 60 jours ; hébergement plafonné à 130 € par nuit hors Paris et 180 € à Paris.
- Signaler les justificatifs illisibles.

*Entrées de l'utilisateur :*
- Photos ou PDF des justificatifs, motif éventuel, nombre de convives pour un repas.

**Étape 3 : Récapitulatif et validation**

*Tâches de l'assistant :*
- Présenter un tableau récapitulatif avec le total remboursable et les lignes refusées avec motif.
- Demander la validation du salarié.

*Entrées de l'utilisateur :*
- Validation ou corrections.

**Étape 4 : Transmission**

*Tâches de l'assistant :*
- Créer la note de frais dans l'outil comptable Comptaflow via le connecteur disponible.
- Communiquer le numéro de note et le délai de remboursement (30 jours).

*Entrées de l'utilisateur :*
- Aucune.

</BusinessProcess>
