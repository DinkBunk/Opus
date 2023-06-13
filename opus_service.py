import uuid

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

        db_conn = psycopg2.connect(host=host, database="opus-db", user=username,
                                   password=password)

        # Create an instance of the BlobDelegate class
        self.blob_delegate = BlobDelegate("opus-training-data")

        # Create an instance of the MixDelegate class
        self.mix_delegate = MixDelegate(session)

        # Create an instance of the StemDelegate class
        self.stem_delegate = StemDelegate(session)

    def process_upload(self, file, metadata, is_stem):
        blob_id = str(uuid.uuid4())
        self.blob_delegate.upload_blob(blob_id, file)
        if is_stem:
            self.stem_delegate.create_stem(blob_id, metadata['artist'], metadata['title'], metadata['instrument'],
                                           metadata['mix_id'], blob_id)
        else:
            self.mix_delegate.create_mix(blob_id, metadata['artist'], metadata['title'], blob_id)

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

    def get_audio_by_id(self, blob_id):
        return self.blob_delegate.get_blob(blob_id)

    def get_all_stems(self):
        return self.stem_delegate.get_all_stems()