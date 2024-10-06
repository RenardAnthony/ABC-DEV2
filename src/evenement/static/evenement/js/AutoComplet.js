document.addEventListener('DOMContentLoaded', function() {

    const lieuField = document.getElementById('id_lieu');
    const adresseField = document.getElementById('adresse');

    function updateAdresseField() {
        const selectedOption = lieuField.options[lieuField.selectedIndex];

        if (selectedOption.value === "autre") {
            adresseField.value = '';
            adresseField.readOnly = false;
        } else {
            const adresse = selectedOption.getAttribute('data-adresse');
            if (adresse) {
                adresseField.value = adresse;
                adresseField.readOnly = true;
            } else {
                adresseField.value = '';
                adresseField.readOnly = true;
            }
        }
    }

    updateAdresseField();
    lieuField.addEventListener('change', updateAdresseField);

    function toggleReadonlyFields() {
        document.querySelectorAll('input[type="checkbox"][name="type_replique_autorisee"]').forEach(function(checkbox) {
            const replique = checkbox.value;
            const limiteField = document.getElementById(`limite_${replique}`);

            if (checkbox.checked) {
                limiteField.removeAttribute('readonly');
            } else {
                limiteField.setAttribute('readonly', 'readonly');
                limiteField.value = 0;
            }
        });

        const freelanceCheckbox = document.getElementById('freelance');
        const prixFreelanceField = document.getElementById('prix_freelance');
        const locationsCheckbox = document.getElementById('locations');
        const prixLocationField = document.getElementById('prix_location');
        const repasCheckbox = document.getElementById('repas');
        const prixRepasField = document.getElementById('prix_repas');

        if (freelanceCheckbox.checked) {
            prixFreelanceField.removeAttribute('readonly');
        } else {
            prixFreelanceField.setAttribute('readonly', 'readonly');
            prixFreelanceField.value = 0;
        }

        if (locationsCheckbox.checked) {
            prixLocationField.removeAttribute('readonly');
        } else {
            prixLocationField.setAttribute('readonly', 'readonly');
            prixLocationField.value = 0;
        }

        if (repasCheckbox.checked) {
            prixRepasField.removeAttribute('readonly');
        } else {
            prixRepasField.setAttribute('readonly', 'readonly');
            prixRepasField.value = 0;
        }
    }

    toggleReadonlyFields();
    document.getElementById('freelance').addEventListener('change', toggleReadonlyFields);
    document.getElementById('locations').addEventListener('change', toggleReadonlyFields);
    document.getElementById('repas').addEventListener('change', toggleReadonlyFields);

    document.querySelectorAll('input[type="checkbox"][name="type_replique_autorisee"]').forEach(function(checkbox) {
        checkbox.addEventListener('change', toggleReadonlyFields);
    });
});
