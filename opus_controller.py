from flask import Flask, request, render_template, jsonify, make_response
import uuid
import os
from werkzeug.utils import secure_filename
from tensor_tools import chunkify, apply_transform

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("app.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    # if 'file' not in request.files:
    #     return "No file part", 400
    song_name = request.form.get("song_name", "unnamed")
    file = request.files['audio_file']
    song_data = save_uploaded_files(song_name, [file])
    return jsonify(song_data)


@app.route('/dataset', methods=['GET'])
def get_datasets():
    files = []
    for folder in os.listdir("dataset"):
        for file in os.listdir(os.path.join("dataset", folder)):
            if file.endswith(".wav"):
                files.append(os.path.join(folder, file))
    response = make_response(jsonify(files))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/upload-folder', methods=['POST'])
def upload_folder():
    if 'files[]' not in request.files:
        return "No file part", 400

    song_name = request.form.get("song_name", "unnamed")
    files = request.files.getlist('files[]')
    song_data = save_uploaded_files(song_name, files)
    return jsonify(song_data)


@app.route('/song-chunks', methods=['POST'])
def get_chunks():
    song_id = request.json.get('song_id')
    song_path = os.path.join("dataset", song_id, song_id + ".wav")
      = chunkify(song_path, 2000)
    return jsonify({'chunks': chunked_waveforms})

@app.route('/apply-transformation', methods=['POST'])
def apply_transformation_route():
    content = request.json
    chunk_waveform = content['chunk_waveform']
    transform_type = content['transform_type']

    transformed_waveform = apply_transform(chunk_waveform, transform_type)
    return jsonify({'transformed_waveform': transformed_waveform})

def save_uploaded_files(song_name, files):
    song_id = str(uuid.uuid4())
    song_path = os.path.join("dataset", song_id)
    os.makedirs(song_path)

    song_data = {
        'song_id': song_id,
        'song_name': song_name,
    }

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(song_path, filename)
        file.save(file_path)
        song_data[filename] = file_path
    return song_data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
