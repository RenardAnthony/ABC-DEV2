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



// Gestion des actions sur les messages
document.addEventListener('click', function (event) {
    // Suppression d'un message
    if (event.target.classList.contains('btn-delete')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const deleteUrl = `/commentaires/delete/${messageId}/`;

        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const messageElement = document.getElementById(`message-${messageId}`);
                messageElement.innerHTML = '<em>Ce message a été supprimé</em>';
                messageElement.classList.add('deleted');
            } else {
                console.error('Erreur de suppression :', data.error);
            }
        })
        .catch(error => console.error('Erreur réseau :', error));
    }

    // Modification d'un message
    if (event.target.classList.contains('btn-edit')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const messageElement = document.getElementById(`message-${messageId}`);
        const messageContentElement = messageElement.querySelector('.message-content p');

        // Vérifie si une édition est déjà en cours
        if (messageElement.querySelector('.edit-textarea')) {
            console.warn('Une édition est déjà en cours pour ce message.');
            return;
        }

        const currentContent = messageContentElement.textContent.trim();

        // Remplace le contenu par un champ de texte éditable
        messageContentElement.innerHTML = `
            <textarea class="edit-textarea">${currentContent}</textarea>
            <button class="btn-save-edit" data-message-id="${messageId}">Enregistrer</button>
            <button class="btn-cancel-edit" data-message-id="${messageId}">Annuler</button>
        `;
    }

    // Sauvegarde de la modification d'un message
    if (event.target.classList.contains('btn-save-edit')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const saveUrl = `/commentaires/edit/${messageId}/`;
        const textarea = event.target.parentElement.querySelector('.edit-textarea');
        const newContent = textarea.value.trim();

        fetch(saveUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ content: newContent }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const messageElement = document.getElementById(`message-${messageId}`);
                const messageContentElement = messageElement.querySelector('.message-content');

                messageContentElement.innerHTML = `
                    <p>${data.updated_content}</p>
                    <p class="edited-tag">Édité</p>
                `;
            } else {
                console.error('Erreur lors de la modification :', data.error);
            }
        })
        .catch(error => console.error('Erreur réseau ou serveur :', error));
    }

    // Annulation de la modification d'un message
    if (event.target.classList.contains('btn-cancel-edit')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const messageElement = document.getElementById(`message-${messageId}`);
        const messageContentElement = messageElement.querySelector('.message-content');
        const originalContent = messageContentElement.dataset.originalContent;

        // Réinitialiser le contenu original
        messageContentElement.innerHTML = `<p>${originalContent}</p>`;
    }
});