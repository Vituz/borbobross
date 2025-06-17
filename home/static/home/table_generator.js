document.addEventListener("DOMContentLoaded", function () {

    const numTablesInput = document.getElementById("numTables");
    const playersPerTableInput = document.getElementById("playersPerTable");
    const decreaseTables = document.getElementById("decreaseTables");
    const increaseTables = document.getElementById("increaseTables");
    const decreasePlayers = document.getElementById("decreasePlayers");
    const increasePlayers = document.getElementById("increasePlayers");
    const generateButton = document.getElementById("generateButton");
    const previewSection = document.getElementById("previewSection");
    const tablesPreview = document.getElementById("tablesPreview");
    const regenerateButton = document.getElementById("regenerateButton");

    function handleInputChange(input, min) {
        let value = parseInt(input.value) || 0;
        if (value < min) value = min;
        input.value = value;
    }

    numTablesInput.addEventListener("change", function () {
        handleInputChange(this, 1);
    });

    playersPerTableInput.addEventListener("change", function () {
        handleInputChange(this, 2);
    });

    decreaseTables.addEventListener("click", function () {
        let value = parseInt(numTablesInput.value) || 0;
        if (value > 1) {
        numTablesInput.value = value - 1;
        }
    });

    increaseTables.addEventListener("click", function () {
        let value = parseInt(numTablesInput.value) || 0;
        numTablesInput.value = value + 1;
    });

    decreasePlayers.addEventListener("click", function () {
        const players = document.getElementById('playerList');
        let value = parseInt(playersPerTableInput.value) || 0;
        if (value > 2) {
            playersPerTableInput.value = value - 1;
        }
        players.lastElementChild.remove();
    });

    increasePlayers.addEventListener("click", function () {
        const players = document.getElementById('playerList')
        let value = parseInt(playersPerTableInput.value) || 0;
        console.log(value)

        playersPerTableInput.value = value + 1;
        const newPlayer = `
            <input type="text" name="player" placeholder="Inserisci Nome"
            class="h-5 p-4 w-full border-gray-300 border rounded focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent">
        `
        players.insertAdjacentHTML('beforeend', newPlayer);  
    });
    
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
        }

    generateButton.addEventListener('click', function(){
        generateTable();
    });

    function generateTable(){
        const numbTables = parseInt(document.getElementById('numTables').value) || 2;
        console.log('Tables: ',numbTables);
        const players = document.getElementsByName('player');
        console.log('Players: ', players);
        let playerList = []
        players.forEach(el => {
            playerList.push(el.value);
            console.log(el.value);
        });
        console.log(playerList);
        shuffled_list = shuffleArray(playerList);
        console.log(shuffled_list);
        
        const data = {
            'table_numbers': numbTables,
            'player_list': playerList
        }

        const response = fetch('api/table_generator/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                
            },
            body: JSON.stringify(data)
        })
        .then(response =>{
            if(!response.ok){
                throw new Error('Errore nella risposta del server');
            }
            return response.json();
        })
        .then(result =>{
            console.log('Risultato della chiamata: ', result);
            tablesPreview.innerHTML = '';
            result.tables.forEach(table => {
                // console.log(table);
                const tableDiv = document.createElement("div");
                tableDiv.className = 'bg-gray-50 p-4 rounded-lg border border-gray-200';

                const tableHeader = document.createElement('h3');
                tableHeader.className = 'text-lg font-semibold text-primary mb-3 pb-2 border-b border-gray-200';
                tableHeader.textContent = `Tavolo ${result.tables.indexOf(table) + 1}`;

                console.log('Numero: ', result.tables.indexOf(table) + 1);

                const tablePlayerList = document.createElement('ul');
                tablePlayerList.className = 'space-y-2';

                table.forEach(player =>{
                    const playerName = player;
                    const playerItem = document.createElement('li');
                    playerItem.className = 'flex items-center';
                    const playerIcon = document.createElement('div');
                    playerIcon.className = 'w-6 h-6 flex items-center justify-center mr-2 text-gray-600';
                    playerIcon.innerHTML = '<i class="ri-user-line"></i>';
                    
                    const playerText = document.createElement('span');
                    playerText.textContent = playerName;
                    
                    playerItem.appendChild(playerIcon);
                    playerItem.appendChild(playerText);
                    tablePlayerList.appendChild(playerItem);
                    console.log('Nuovo Giocatore aggiunto: ', player)
                });

                tableDiv.appendChild(tableHeader);
                tableDiv.appendChild(tablePlayerList);
                tablesPreview.appendChild(tableDiv);
                console.log('Nuovo tavolo aggiunto');
            });
            previewSection.classList.remove('hidden');
                
            // Scroll to preview section
            previewSection.scrollIntoView({ behavior: 'smooth' });
            
        })
        .catch(error =>{
            console.error('Errore nella chiamata: ', error);
        });

        
        

    }

    regenerateButton.addEventListener('click', function(){
        generateTable();
    });

});