document.addEventListener('DOMContentLoaded', function () {
    const yearFilter = document.getElementById('yearFilter');
    const yearSections = document.querySelectorAll('section > div');
    yearFilter.addEventListener('change', function () {
        const selectedYear = this.value;
        if (selectedYear === 'all') {
            yearSections.forEach(section => {
                section.style.display = 'block';
            });
        } else {
            yearSections.forEach(section => {
                const yearHeading = section.querySelector('h2');
                if (yearHeading && yearHeading.textContent === selectedYear) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const deleteConfirmModal = document.getElementById('deleteConfirmModal');
    const cancelDeleteBtn = document.getElementById('cancelDelete');
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    let gameToDelete = null;
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            matchId = this.id;
            e.preventDefault();
            e.stopPropagation();
            gameToDelete = this.closest('.game-card');
            
            deleteConfirmModal.classList.remove('hidden');
        });
    });
    cancelDeleteBtn.addEventListener('click', function () {
        deleteConfirmModal.classList.add('hidden');
        gameToDelete = null;
    });
    confirmDeleteBtn.addEventListener('click', function () {
        if (gameToDelete) {
            deleteMatchFromDb(matchId);
            // Animazione di rimozione
            gameToDelete.style.opacity = '0';
            gameToDelete.style.transform = 'scale(0.9)';
            gameToDelete.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            setTimeout(() => {
                gameToDelete.remove();
                // Controlla se la sezione dell'anno è vuota
                const yearSections = document.querySelectorAll('section > div');
                yearSections.forEach(section => {
                    const cards = section.querySelectorAll('.game-card');
                    if (cards.length === 0) {
                        section.style.display = 'none';
                    }
                });
                gameToDelete = null;
            }, 300);
            deleteConfirmModal.classList.add('hidden');
        }
    });
    // Chiudi il modal cliccando fuori
    deleteConfirmModal.addEventListener('click', function (e) {
        if (e.target === this) {
            deleteConfirmModal.classList.add('hidden');
            gameToDelete = null;
        }
    });

    async function deleteMatchFromDb(id){
        const data = {'id' : id}
        console.log('Match id: ', data)
        try{
            const response = await fetch('api/delete_match/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken' : getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });

            if(!response.ok){
                const errorData = await response.json();
                throw new Error(`Errore HTTP! Status: ${response.status}, Messaggio: ${errorData.message || 'Errore sconosciuto'}`);
            }
            const result = await response.json();
            console.log('Match eliminato con successo:', result);
            return result;
        }catch(error){
            console.error('Si è verificato un errore durante l\'eliminazione del match:', error);
            throw error;
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



document.addEventListener('DOMContentLoaded', function () {
    const addGameBtn = document.getElementById('addGameBtn');
    const addGameModal = document.getElementById('addGameModal');
    const closeModalBtn = document.getElementById('closeModal');
    const cancelAddGameBtn = document.getElementById('cancelAddGame');
    const addParticipantBtn = document.getElementById('addParticipant');
    const participantsContainer = document.getElementById('participantsContainer');
    const addGameForm = document.getElementById('addGameForm');
    let participantCount = 1;
    // Apri il modal
    addGameBtn.addEventListener('click', function () {
        addGameModal.classList.remove('hidden');
    });
    // Chiudi il modal
    const closeModal = function () {
        addGameModal.classList.add('hidden');
        addGameForm.reset();
        // Resetta i partecipanti
        while (participantsContainer.children.length > 1) {
            participantsContainer.removeChild(participantsContainer.lastChild);
        }
        participantCount = 1;
    };
    closeModalBtn.addEventListener('click', closeModal);
    cancelAddGameBtn.addEventListener('click', closeModal);
    // Chiudi il modal cliccando fuori
    addGameModal.addEventListener('click', function (e) {
        if (e.target === this) {
            closeModal();
        }
    });
    // Aggiungi partecipante
    addParticipantBtn.addEventListener('click', function () {
        participantCount++;
        const newParticipant = document.createElement('div');
        newParticipant.className = 'participant-entry grid grid-cols-1 md:grid-cols-2 gap-4 mb-3 relative';
        newParticipant.innerHTML = `
                                    <div>
                                    <label for="participant${participantCount}" class="block text-sm font-medium text-gray-700 mb-1">Nome Partecipante</label>
                                    <input type="text" id="participant${participantCount}" class="w-full px-4 py-2 border border-gray-300 !rounded-button focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary" required>
                                    </div>
                                    <div class="relative">
                                    <label for="deck${participantCount}" class="block text-sm font-medium text-gray-700 mb-1">Deck Utilizzato</label>
                                    <input type="text" id="deck${participantCount}" class="w-full px-4 py-2 border border-gray-300 !rounded-button focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary" required>
                                    <button type="button" class="remove-participant absolute top-9 right-0 -mt-1 mr-2 text-red-500 hover:text-red-700">
                                    <div class="w-5 h-5 flex items-center justify-center">
                                    <i class="ri-close-circle-line"></i>
                                    </div>
                                    </button>
                                    </div>
                                    `;
        participantsContainer.appendChild(newParticipant);
        // Aggiungi evento per rimuovere il partecipante
        const removeBtn = newParticipant.querySelector('.remove-participant');
        removeBtn.addEventListener('click', function () {
            participantsContainer.removeChild(newParticipant);
        });
    });
    // Gestisci l'invio del form
    addGameForm.addEventListener('submit', function (e) {
        e.preventDefault();
        // Qui dovresti inviare i dati al server
        // Per ora, simuliamo l'aggiunta di una nuova partita
        const winnerName = document.getElementById('winnerName').value;
        const winnerDeck = document.getElementById('winnerDeck').value;
        // const gameDate = document.getElementById('gameDate').value;
        // Raccogli i partecipanti
        let participantsHTML = '';
        const participantEntries = document.querySelectorAll('.participant-entry');
        let participants = []
        participantEntries.forEach(entry => {
            const participantInput = entry.querySelector('input[id^="participant"]');
            const deckInput = entry.querySelector('input[id^="deck"]');
            participants.push({
                playerName: participantInput.value,
                deckName: deckInput.value
            })
            console.log(participantInput.value);
            console.log(deckInput.value);
        });
        // Chiudi il modal
        async function addMatchOnDb(winnerName, winnerDeck, participants) {
            data = {
                'winner_name':winnerName, 
                'winner_deck': winnerDeck,
                'participants': participants
            }

            try{
                const response = await fetch('api/save_match/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify(data)
                });

                if(!response.ok){
                    const errorData = await response.json();
                    throw new Error('Errore HTTP! Status: ', response.status, ' Messaggio: ', errorData.message);
                    
                }
                const result = await response.json();
                console.log('Dati inviati con successo: ', result);
                return result;
            }catch(error){
                console.error('Si è verificato un errore durante l\'invio dei dati:', error);
                throw error;
            }
            
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        addMatchOnDb(winnerName, winnerDeck, participants);
        closeModal();
        // location.reload();
    });
});