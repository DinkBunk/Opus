from flask import Flask, request, render_template, jsonify, send_from_directory
import uuid
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("app.html")


@app.route('/upload-folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        return "No file part", 400

    song_name = request.form.get("song_name", "unnamed")
    files = request.files.getlist('files[]')
    song_data = save_uploaded_files(song_name, files)
    return jsonify(song_data)


def save_uploaded_files(song_name, files):
    song_id = str(uuid.uuid4())
    song_dir = os.path.join("dataset", song_id, song_name)
    stems_dir = os.path.join(song_dir, "stems")

    # Create the main song directory and the 'stems' subdirectory if they don't exist
    os.makedirs(song_dir, exist_ok=True)
    os.makedirs(stems_dir, exist_ok=True)

    song_file = None
    stem_files = []

    for file in files:
        filename = secure_filename(file.filename)
        if 'stem' in filename.lower():
            filepath = os.path.join(stems_dir, filename)
            file.save(filepath)
            stem_files.append(filepath)
        else:
            filepath = os.path.join(song_dir, filename)
            file.save(filepath)
            song_file = filepath

    return {
        'song_id': song_id,
        'song_name': song_name,
        'song_path': song_file,
        'stems': stem_files
    }


@app.route('/song-chunks/<song_id>', methods=['GET'])
def get_chunks(song_id):
    chunked_waveforms = chunkify_song(song_id)
    return jsonify({'chunks': chunked_waveforms})


def chunkify_song(song_id):
    # Implement a function to load the song using song_id,
    # split it into chunks, and return the waveforms as a list
    pass


@app.route('/apply-transformation', methods=['POST'])
def apply_transformation_route():
    content = request.json
    chunk_waveform = content['chunk_waveform']
    transform_type = content['transform_type']

    transformed_waveform = apply_transformation(chunk_waveform, transform_type)
    return jsonify({'transformed_waveform': transformed_waveform})


def apply_transformation(chunk_waveform, transform_type):
    # Implement a function to apply the specified transformation to the chunk_waveform
    pass


@app.route('/uploaded-folders', methods=['GET'])
def get_uploaded_folders():
    base_path = "dataset"  # This should be the same path where you store the uploaded folders
    folders = os.listdir(base_path)

    folder_data = []
    for folder in folders:
        song_dir = os.path.jwoin(base_path, folder)
        if os.path.isdir(song_dir):
            song_name = os.path.basename(song_dir)
            song_id = folder
            folder_data.append({"song_id": song_id, "song_name": song_name})

    return jsonify(folder_data)


@app.route('/train/<song_id>', methods=['POST'])
def train_route(song_id):
    # Implement training logic here, and train the model
    train_model(song_id)
    return jsonify({"success": True})


def train_model(song_id):
    # Implement a function to load song, stems, pre-processed chunks,
    # and train the model accordingly
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
