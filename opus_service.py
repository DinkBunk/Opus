import uuid
from builtins import Exception

import psycopg2
from blob_delegate import BlobDelegate
from stem_delegate import StemDelegate
from mix_delegate import MixDelegate
from database import session

import tensor_tools as tt
import os

username = os.environ.get('GOOGLE_DB_USER')
password = os.environ.get('GOOGLE_DB_PASS')
host = os.environ.get('GOOGLE_DB_HOST')


class OpusService:
    def __init__(self):

        db_conn = psycopg2.connect(host="34.69.202.204", database="opus-db", user="opus-service", password="BltDdup_8782")


        # Create an instance of the BlobDelegate class
        self.blob_delegate = BlobDelegate("opus-training-data")

        # Create an instance of the MixDelegate class
        self.mix_delegate = MixDelegate(session)

        # Create an instance of the StemDelegate class
        self.stem_delegate = StemDelegate(session)


    def process_upload(self, file, metadata):
        blob_id = str(uuid.uuid4())
        metadata['id'] = blob_id
        self.blob_delegate.upload_blob(blob_id, file)
        try:
            if metadata['type'] == 'stem' and metadata['instrument']:
                self.stem_delegate.create_stem(blob_id, metadata['artist'], metadata['title'], metadata['instrument'],
                                           metadata['parent_mix_id'])
            else:
                self.mix_delegate.create_mix(blob_id, metadata['artist'], metadata['title'], metadata['parent_mix_id'])
        except Exception as e:
            return {'exception': str(e)}, 400

        return metadata

    def search_all_entries(self, search_term):
        mixes = self.mix_delegate.search_by_artist_or_title(search_term)
        stems = self.stem_delegate.search_by_artist_or_title(search_term)
        return mixes, stems

    def get_stems_for_mix(self, mix_id):
        ids = self.mix_delegate.get_stems_for_mix(mix_id)
        stems = []
        for id in ids:
            stems.append(self.stem_delegate.get_stem(id))
    def get_stem_metadata(self, stem_id):
        return self.stem_delegate.get_stem(stem_id)

    def get_mix_metadata(self, mix_id):
        return self.mix_delegate.get_mix(mix_id)


    def get_all_stems(self):
        return self.stem_delegate.get_all_stems()

    def get_waveform(self, blob_id, filename):
        path = self.blob_delegate.download_blob(blob_id, filename)
        whole, chunks = tt.chunkify(path, 1000)
        return whole, chunks

    def get_all_mixes(self):
        return self.mix_delegate.get_all_mixes()