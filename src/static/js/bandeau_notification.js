// Afficher un bandeau de notification
function showNotification(type, message) {
    var notification = document.getElementById('notification');

    // Appliquer le type de notification
    notification.className = type + ' show';

    // Ajouter le message
    notification.querySelector('p').textContent = message;

    // Afficher le texte "cliquer pour cacher" si le message est long
    if (message.length > 40) {
        const clickToHide = document.createElement('span');
        clickToHide.textContent = 'cliquer pour cacher';
        clickToHide.style.color = 'gray';
        clickToHide.style.fontSize = '12px';
        clickToHide.style.marginLeft = 'auto';
        notification.querySelector('p').appendChild(clickToHide);

        // Ajouter un événement de clic pour cacher la notification
        notification.addEventListener('click', hideNotification);
    } else {
        // Cacher la notification après 3 secondes pour les messages courts
        setTimeout(function () {
            notification.style.opacity = '0';
            notification.style.left = '-100%';
            notification.classList.remove('show');
        }, 3000);
    }

    // Afficher la notification
    notification.style.left = '10%';
    notification.style.opacity = '1';
}

// Fermer la notification
function hideNotification() {
    const notification = document.getElementById('notification');
    notification.style.opacity = '0';
    notification.style.left = '-100%';
    notification.classList.remove('show');

    // Supprimer l'événement de clic après fermeture pour éviter des conflits futurs
    notification.removeEventListener('click', hideNotification);
}




window.addEventListener('resize', function() {
    if (window.innerWidth <= 700) {
        document.querySelector('header.pc').style.display = 'none';
        document.querySelector('header.mobil').style.display = 'flex';
    } else {
        document.querySelector('header.pc').style.display = 'flex';
        document.querySelector('header.mobil').style.display = 'none';
    }
});

// Simule un redimensionnement pour forcer l'application des styles au chargement
window.dispatchEvent(new Event('resize'));

//showNotification('success', 'Votre inscription a été confirmée.'); en ajax

//messages.success(request, "Formulaire envoyé avec succès !")
//messages.error(request, "Erreur lors de l'envoi du formulaire.")
//messages.warning(request, "Attention : Action importante requise.")
//messages.info(request, "Bienvenue sur votre tableau de bord.")