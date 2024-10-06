// Récupère l'élément de la div
var btn_adi = document.getElementById('button_aditionnel');

// Initialise l'état de la div à caché
btn_adi.style.display = 'none';

// Fonction pour basculer l'affichage de la div
function btn_adi_toggle() {
    if (btn_adi.style.display === 'none' || btn_adi.style.display === '') {
        btn_adi.style.display = 'flex'; // Affiche la div
    } else {
        btn_adi.style.display = 'none'; // Cache la div
    }
}