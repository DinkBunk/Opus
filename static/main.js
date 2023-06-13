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

function uploadSong() {
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a file to upload');
        return;
    }
    const artistInput = document.getElementById('artist');
    const titleInput = document.getElementById('title');
    const instrumentInput = document.getElementById('instrument');
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