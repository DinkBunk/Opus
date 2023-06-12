import uuid
from flask import Flask, request, render_template, jsonify, make_response
from tensor_tools import chunkify, apply_transform
from service.opus_service import OpusService
from models.models import Session, Stem

app = Flask(__name__)
service = OpusService()

@app.route('/')
def index():
    return render_template("app.html")


@app.route('/upload', methods=['POST'])
def upload_stem():
    if 'file' not in request.files or 'metadata' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    file = request.files['file']
    metadata = request.json['metadata']

    session = Session()

    new_stem = Stem(stem_id=str(uuid.uuid4()), artist=metadata['artist'], title=metadata['title'], instrument=metadata['instrument'], mix_id=metadata['mix_id'], blob_id="Blob ID")
    session.add(new_stem)
    session.commit()

    session.close()

    return jsonify({'message': 'Stem uploaded successfully'}), 201

@app.route('/songs/<blob_id>', methods=['GET'])
def get_song_data(blob_id):
    song_data = service.get_song_data(blob_id)
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/songs', methods=['GET'])
def get_all_metadata():
    song_data = service.get_all_metadata()
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/search', methods=['GET'])
def search_all():
    search_term = request.args.get('q')
    song_data = service.search_all(search_term)
    return jsonify(song_data), 200

@app.route('/chunkify/<blob_id>', methods=['GET'])
def get_song_chunks(blob_id):
    song_data = service.get_song_data(blob_id)
    chunks = chunkify(song_data['blob_id'], 1000)
    return jsonify(chunks), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)


