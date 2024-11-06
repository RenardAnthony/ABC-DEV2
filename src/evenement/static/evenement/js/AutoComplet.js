document.addEventListener('DOMContentLoaded', function () {
    // Fonction pour basculer l'état d'une réplique
    const repliqueArticles = document.querySelectorAll('.replique-section');
    const hiddenInput = document.getElementById('type_replique_autorisee_hidden');

    function toggleReplique(article) {
        const repliqueId = article.getAttribute('data-replique-id');
        const limiteField = document.getElementById(`limite_${repliqueId}`);

        // Basculer l'état actif de l'article
        if (article.classList.contains('active')) {
            article.classList.remove('active');
            limiteField.setAttribute('readonly', 'readonly');
            limiteField.value = 0;
            article.style.opacity = '0.2';
        } else {
            article.classList.add('active');
            limiteField.removeAttribute('readonly');
            article.style.opacity = '1';
        }

        // Mise à jour du champ caché global pour refléter la sélection actuelle
        updateHiddenRepliqueField();
    }

    function updateHiddenRepliqueField() {
        const selectedRepliques = Array.from(repliqueArticles)
            .filter(article => article.classList.contains('active'))
            .map(article => article.getAttribute('data-replique-id'));

        hiddenInput.value = selectedRepliques.join(',');
    }

    repliqueArticles.forEach(article => {
        article.addEventListener('click', function (event) {
            // Éviter de désactiver la réplique si l'élément cliqué est un champ d'entrée
            if (!event.target.matches('input[type="number"]')) {
                toggleReplique(article);
            }
        });
    });

    // Initialiser le champ caché avec les répliques sélectionnées au chargement de la page
    updateHiddenRepliqueField();

    // Gestion de l'adresse
    const lieuField = document.getElementById('id_lieu');
    const adresseField = document.getElementById('adresse');

    function updateAdresseField() {
        const selectedOption = lieuField.options[lieuField.selectedIndex];

        if (selectedOption.value === 'autre') {
            // L'utilisateur a choisi 'autre', il doit entrer une adresse manuellement
            adresseField.value = '';
            adresseField.readOnly = false;
        } else {
            // Pré-remplir l'adresse selon le lieu sélectionné
            const adresse = selectedOption.getAttribute('data-adresse');
            adresseField.value = adresse || '';
            adresseField.readOnly = true;
        }
    }

    if (lieuField && adresseField) {
        updateAdresseField();  // Initialisation au chargement
        lieuField.addEventListener('change', updateAdresseField);  // Mise à jour au changement
    }

    // Gestion des champs readonly pour les autres options
    function toggleReadonlyFields() {
        // Gérer les champs de prix pour les options
        const freelanceCheckbox = document.getElementById('freelance');
        const prixFreelanceField = document.getElementById('prix_freelance');
        const locationsCheckbox = document.getElementById('locations');
        const prixLocationField = document.getElementById('prix_location');
        const prixRepasField = document.getElementById('prix_repas');

        if (freelanceCheckbox && prixFreelanceField) {
            prixFreelanceField.readOnly = !freelanceCheckbox.checked;
            if (!freelanceCheckbox.checked) prixFreelanceField.value = 0;
        }

        if (locationsCheckbox && prixLocationField) {
            prixLocationField.readOnly = !locationsCheckbox.checked;
            if (!locationsCheckbox.checked) prixLocationField.value = 0;
        }

        // Gérer l'option de repas et son prix pour les boutons radio
        const repasRadios = document.querySelectorAll('input[name="repas"]');
        if (repasRadios && prixRepasField) {
            const repasInclus = Array.from(repasRadios).some(radio => radio.checked && radio.value === 'Inclus');
            prixRepasField.readOnly = !repasInclus;
            if (!repasInclus) prixRepasField.value = 0;
        }
    }

    toggleReadonlyFields();

    // Ajouter les événements pour déclencher la mise à jour des champs
    document.querySelectorAll('#freelance, #locations, input[name="repas"]').forEach(element => {
        element.addEventListener('change', toggleReadonlyFields);
    });
});
