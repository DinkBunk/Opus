window.onload = function() {
    // Populate the song list
    fetch('/songs')
        .then(response => response.json())
        .then(songs => {
            const select = document.getElementById('songs');
            songs.forEach(song => {
                const option = document.createElement('option');
                option.value = song.blob_id;
                option.textContent = song.title;
                select.appendChild(option);
            });
            select.onchange = selectSong;  // Add event listener for song selection
        });
};

// Handle song selection
function selectSong(event) {
    const blob_id = event.target.value;
    fetch(`/chunkify/${blob_id}`)
        .then(response => response.json())
        .then(chunks => {
            const display = document.getElementById('chunk-display');
            display.innerHTML = '';
            chunks.forEach(chunk => {
                const div = document.createElement('div');
                div.textContent = chunk.id;
                div.onclick = () => selectChunk(chunk);
                display.appendChild(div);
            });
        });
}

function uploadStem() {
    const fileInput = document.getElementById('stem-file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload');
        return;
    }
    const artistInput = document.getElementById('stem-artist');
    const titleInput = document.getElementById('stem-title');
    const instrumentInput = document.getElementById('stem-instrument');
    const mixIdInput = document.getElementById('mix_id');
    const formData = new FormData();
    formData.append('file', file);
    // Add the metadata from the inputs
    formData.append('metadata', JSON.stringify({
        artist: artistInput.value,
        title: titleInput.value,
        instrument: instrumentInput.value,
        mix_id: mixIdInput.value
    }));
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else if (data.error) {
                alert(data.error);
            }
        });
}

// Handle chunk selection
function selectChunk(chunk) {
    const display = document.getElementById('waveform-display');
    display.innerHTML = '';
    // Display the chunk waveform
}

// Apply a transform
function applyTransform(transformName) {
    const blob_id = document.getElementById('songs').value;
    fetch(`/apply_transform/${blob_id}?transform=${transformName}`)
        .then(response => response.json())
        .then(transformedChunk => {
            const display = document.getElementById('waveform-display');
            display.innerHTML = '';
            // Display the transformed chunk waveform
        });
}

function search(keyword) {
    fetch(`/search?keyword=${keyword}`)
        .then(response => response.json())
        .then(searchResults => {
            // Process the search results
            displaySearchResults(searchResults);
        })
        .catch(error => {
            console.error('Error searching:', error);
        });
}

function displaySearchResults(searchResults) {
    const mixesContainer = document.getElementById('mixes-container');
    mixesContainer.innerHTML = ''; // Clear previous mix items

    searchResults.forEach(result => {
        const mixItem = document.createElement('div');
        mixItem.classList.add('mix-item');
        mixItem.dataset.itemId = result.id;
        mixItem.textContent = result.name;

        mixesContainer.appendChild(mixItem);
    });
}

function getWavFile(itemId) {
    fetch(`/get/${itemId}`)
        .then(response => response.blob())
        .then(wavBlob => {
            // Process the WAV blob
            displayWaveform(wavBlob);
        })
        .catch(error => {
            console.error('Error getting WAV file:', error);
        });
}

const mixesContainer = document.getElementById('mixes-container');

mixesContainer.addEventListener('dblclick', event => {
    const item = event.target;
    if (item.classList.contains('mix-item')) {
        const itemId = item.dataset.itemId;
        getWavFile(itemId);
    }
});

mixesContainer.addEventListener('dblclick', event => {
    const item = event.target;
    if (item.classList.contains('mix-item')) {
        const itemId = item.dataset.itemId;
        getWavFile(itemId);
    }
});

// Remove noise
function removeNoise() {
    const blob_id = document.getElementById('songs').value;
    fetch(`/remove_noise/${blob_id}`)
        .then(response => response.json())
        .then(cleanedChunk => {
            const display = document.getElementById('waveform-display');
            display.innerHTML = '';
            // Display the cleaned chunk waveform
        });
}