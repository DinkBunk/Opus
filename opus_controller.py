import tensor_tools as tt
import uuid
from flask import Flask, request, render_template, jsonify, make_response
from tensor_tools import chunkify
from opus_service import OpusService


app = Flask(__name__)
service = OpusService()

@app.route('/')
def index():
    return render_template("app.html")


@app.route('/stems', methods=['POST'])
def upload_stem():
    file = request.files['file']
    metadata = request.form
    service.process_upload(file, metadata, True)
    return jsonify({'message': 'success'}), 200

@app.route('/stems/<blob_id>', methods=['GET'])
def get_stem_metadata(blob_id):
    song_data = service.get_stem_metadata(blob_id)
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/stems', methods=['GET'])
def get_all_stems():
    song_data = service.get_stem_metadata()
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/mixes', methods=['GET'])
def get_all_mixes():
    song_data = service.get_all_mixes()
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/mixes', methods=['POST'])
def upload_mix():
    file = request.files['file']
    metadata = request.form
    service.process_upload(file, metadata, False)

    return jsonify({'message': 'success'}), 200


@app.route('/mixes/<blob_id>', methods=['GET'])
def get_mix_metadata(blob_id):
    song_data = service.get_stem_metadata(blob_id)
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/search', methods=['GET'])
def search_all():
    search_term = request.args.get('q')
    song_data = service.search_all_entries(search_term)
    response = make_response(jsonify(song_data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/mixes/<mix_id>/stems', methods=['GET'])
def get_stems_for_mix(mix_id):
    stem_ids = service.get_stems_for_mix(mix_id)
    stems = [service.get_stem_metadata(stem_id) for stem_id in stem_ids]
    response = make_response(jsonify(stems), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def transform_waveform(waveform, sample_rate, transform_type, transform_params):
    return tt.transform_waveform(waveform, sample_rate)


def get_waveform(blob_id, filename):
    return service.get_waveform(blob_id, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)


