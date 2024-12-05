document.addEventListener('click', function (event) {
    // Gestion de la suppression d'un message
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
                console.error('Erreur de suppression : ', data.error);
            }
        })
        .catch(error => console.error('Erreur réseau : ', error));
    }

    // Gestion de la modification d'un message
    if (event.target.classList.contains('btn-edit')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const messageElement = document.getElementById(`message-${messageId}`);
        const currentContent = messageElement.querySelector('.message-content').textContent;

        // Remplace le contenu par un champ de texte éditable
        messageElement.querySelector('.message-content').innerHTML = `
            <textarea class="edit-textarea">${currentContent}</textarea>
            <button class="btn-save-edit" data-message-id="${messageId}">Enregistrer</button>
        `;
    }

    // Sauvegarde de la modification d'un message
    if (event.target.classList.contains('btn-save-edit')) {
        event.preventDefault();

        const messageId = event.target.dataset.messageId;
        const saveUrl = `/commentaires/edit/${messageId}/`;
        const newContent = event.target.previousElementSibling.value;

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
                messageElement.querySelector('.message-content').innerHTML = data.updated_content;
                messageElement.classList.remove('edited');
                messageElement.classList.add('updated');
            }
        });
    }
});


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

document.addEventListener('click', function (event) {
    if (event.target.classList.contains('btn-delete')) {
        console.log('Bouton supprimer cliqué');
        // Le reste du code
    }

    if (event.target.classList.contains('btn-edit')) {
        console.log('Bouton modifier cliqué');
        // Le reste du code
    }
});
