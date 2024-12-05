// Fonction pour récupérer le CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Charger les notifications pour desktop et mobile
function loadNotifications() {
    const desktopBell = document.getElementById('notification-bell');
    const mobileBell = document.getElementById('mobile-notification-bell');
    const desktopBadge = desktopBell ? desktopBell.querySelector('.badge') : null;
    const mobileBadge = mobileBell ? mobileBell.querySelector('.badge') : null;
    const dropdown = document.getElementById('notification-dropdown');

    fetch('/notifications/list/')
        .then(response => response.json())
        .then(data => {
            const count = data.notifications.length;

            // Gérer les badges
            if (count > 0) {
                if (desktopBadge) {
                    desktopBadge.style.display = 'inline';
                    desktopBadge.textContent = count;
                }
                if (mobileBadge) {
                    mobileBadge.style.display = 'inline';
                    mobileBadge.textContent = count;
                    mobileBell.style.display = 'block';
                }
            } else {
                if (desktopBadge) desktopBadge.style.display = 'none';
                if (mobileBadge) mobileBadge.style.display = 'none';
                if (mobileBell) mobileBell.style.display = 'none';
            }

            // Gérer le dropdown (pour desktop uniquement)
            if (dropdown) {
                dropdown.innerHTML = count > 0
                    ? data.notifications.map(notif => `
                        <div class="notification-item" id="notification-${notif.id}">
                            <p>${notif.message}</p>
                            ${notif.redirect_url ? `<a href="${notif.redirect_url}">Voir</a>` : ''}
                            <span class="mark-as-read" data-id="${notif.id}">Marquer comme lu</span>
                        </div>
                    `).join('')
                    : '<p>Aucune notification</p>';
            }
        })
        .catch(error => console.error('Erreur lors du chargement des notifications:', error));
}


// Marquer une notification comme lue
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('mark-as-read')) {
        event.preventDefault();
        const notificationId = event.target.dataset.id;

        if (!notificationId) {
            console.error('ID de notification manquant.');
            return;
        }

        fetch(`/notifications/mark-as-read/${notificationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => {
            if (!response.ok) throw new Error('Erreur serveur.');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Identifier si la notification est desktop ou mobile
                const desktopNotification = document.getElementById(`notification-${notificationId}`);
                const mobileNotification = document.getElementById(`mobile-notification-${notificationId}`);

                // Supprimer l'élément correspondant
                if (desktopNotification) desktopNotification.remove();
                if (mobileNotification) mobileNotification.remove();

                // Réduire le compteur
                const desktopBadge = document.querySelector('#notification-bell .badge');
                const mobileBadge = document.querySelector('#mobile-notification-bell .badge');
                const currentCount = parseInt(desktopBadge?.textContent || '0', 10);

                if (currentCount > 1) {
                    if (desktopBadge) desktopBadge.textContent = currentCount - 1;
                    if (mobileBadge) mobileBadge.textContent = currentCount - 1;
                } else {
                    if (desktopBadge) desktopBadge.style.display = 'none';
                    if (mobileBadge) mobileBadge.style.display = 'none';
                }
            } else {
                console.error('La requête a échoué.');
            }
        })
        .catch(error => console.error('Erreur :', error));
    }
});


// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function () {
    const bell = document.getElementById('notification-bell');
    const mobileBell = document.getElementById('mobile-notification-bell');
    const dropdown = document.getElementById('notification-dropdown');

    // Charger les notifications initiales
    loadNotifications();

    // Gérer le dropdown pour desktop
    if (bell && dropdown) {
        bell.addEventListener('click', function () {
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });
    }

    // Gérer le clic sur la cloche mobile
    if (mobileBell) {
        mobileBell.addEventListener('click', function () {
            alert('Affichage des notifications (adapter selon vos besoins).');
        });
    }

    // Recharger périodiquement les notifications
    setInterval(loadNotifications, 60000); // Toutes les 60 secondes
});

// Charger les notifications pour la version mobile
function loadMobileNotifications() {
    const mobileBell = document.getElementById('notification-bell-mobile');
    const badge = mobileBell.querySelector('.badge');

    fetch('/notifications/list/')
        .then(response => response.json())
        .then(data => {
            if (data.notifications.length > 0) {
                badge.style.display = 'inline';
                badge.textContent = data.notifications.length;
                mobileBell.style.display = 'block'; // Affiche la cloche
            } else {
                badge.style.display = 'none';
                mobileBell.style.display = 'none'; // Cache la cloche
            }
        })
        .catch(error => console.error('Erreur lors du chargement des notifications (mobile) :', error));
}

// Initialisation des notifications mobiles
document.addEventListener('DOMContentLoaded', function () {
    loadMobileNotifications();

    // Recharger périodiquement les notifications
    setInterval(loadMobileNotifications, 60000); // Toutes les 60 secondes
});

document.addEventListener('DOMContentLoaded', function () {
    const mobileBell = document.getElementById('notification-bell-mobile');
    const mobileDropdown = document.getElementById('notification-dropdown_mobil');
    const badge = mobileBell.querySelector('.badge');

    // Charger les notifications
    function loadMobileNotifications() {
        fetch('/notifications/list/')
            .then(response => response.json())
            .then(data => {
                if (data.notifications.length > 0) {
                    badge.style.display = 'inline';
                    badge.textContent = data.notifications.length;
                    mobileBell.style.display = 'block'; // Affiche la cloche
                } else {
                    badge.style.display = 'none';
                    mobileBell.style.display = 'none'; // Cache la cloche
                }

                // Charger les notifications dans le dropdown
                mobileDropdown.innerHTML = ''; // Vider les anciennes notifications
                if (data.notifications.length > 0) {
                    data.notifications.forEach(notif => {
                        const item = document.createElement('div');
                        item.classList.add('notification-item');
                        item.setAttribute('id', `mobile-notification-${notif.id}`); // ID unique pour mobile
                        item.innerHTML = `
                            <p>${notif.message}</p>
                            <div class="notification-actions">
                                ${notif.redirect_url ? `<a href="${notif.redirect_url}">Voir</a>` : ''}
                                <span class="mark-as-read" data-id="${notif.id}">Marquer comme lu</span>
                            </div>
                        `;
                        mobileDropdown.appendChild(item);
                    });
                } else {
                    mobileDropdown.innerHTML = '<p>Aucune notification</p>';
                }
            })
            .catch(error => console.error('Erreur lors du chargement des notifications:', error));
    }

    // Toggle du dropdown
    mobileBell.addEventListener('click', function () {
        if (mobileDropdown.style.display === 'block') {
            mobileDropdown.style.display = 'none';
        } else {
            mobileDropdown.style.display = 'block';
        }
    });

    // Charger les notifications initiales
    loadMobileNotifications();

    // Recharger périodiquement les notifications (optionnel)
    setInterval(loadMobileNotifications, 60000); // Toutes les 60 secondes
});

