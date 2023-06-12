// Populate dataset list
fetch('http://localhost:5000/songs')
    .then(response => response.json())
    .then(data => {
        const datasetList = document.querySelector('#dataset-list');
        data.forEach(song => {
            const li = document.createElement('li');
            li.textContent = `${song.metadata.artist} - ${song.metadata.song_name}`;
            li.dataset.id = song.metadata.blob_id;
            li.addEventListener('dblclick', () => {
                // Call endpoint to chunkify song
                fetch(`http://localhost:5000/chunkify/${song.metadata.blob_id}`)
                    .then(response => response.json())
                    .then(chunks => {
                        // Display chunks in both panels
                        const waveformContainer = document.querySelector('#waveform-container');
                        waveformContainer.innerHTML = '';
                        chunks.forEach(chunk => {
                            const chunkDiv = document.createElement('div');
                            chunkDiv.classList.add('waveform');
                            chunkDiv.textContent = `Chunk ${chunk.id}`;
                            waveformContainer.appendChild(chunkDiv);
                        });
                    });
            });
            datasetList.appendChild(li);
        });
    });

// Handle upload button click
document.querySelector('#upload-button').addEventListener('click', () => {
    const fileField = document.querySelector('#file-field');
    const artistField = document.querySelector('#artist-field');
    const songField = document.querySelector('#song-field');
    const isStemField = document.querySelector('#is-stem-field');
    const instrumentField = document.querySelector('#instrument-field');

    const file = fileField.files[0];
    const artist = artistField.value;
    const song = songField.value;
    const isStem = isStemField.checked;
    const instrument = instrumentField.value;

    const endpoint = isStem ? '/upload/stem' : '/upload/mix';
    const metadata = { artist, song_name: song };
    if (isStem) {
        metadata.instrument = instrument;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    fetch(endpoint, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(songData => {
            // Handle uploaded song data
            const newLi = document.createElement('li');
            newLi.textContent = `${songData.metadata.artist} - ${songData.metadata.song_name}`;
            newLi.dataset.id = songData.metadata.blob_id;
            document.querySelector('#dataset-list').appendChild(newLi);
        });
});

// Handle transform button clicks
document.querySelectorAll('.transform-button').forEach(button => {
    button.addEventListener('click', event => {
        const transform = event.target.dataset.transform;

        // Call /transform endpoint with transform as argument
        fetch(`http://localhost:5000/transform?transform=${transform}`)
            .then(response => response.json())
            .then(data => {
                // Display tensor or plot in viewer
            });
    });
});
