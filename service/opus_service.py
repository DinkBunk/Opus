import uuid
from werkzeug.utils import secure_filename
from delegate.storage_delegate import StorageDelegate
from delegate.metadata_delegate import MetadataDelegate
import tensor_tools as tt
class OpusService:
    def __init__(self):
        self.storage_delegate = StorageDelegate()
        self.metadata_delegate = MetadataDelegate()

    def process_upload(self, file, metadata, is_stem):
        container_id = str(uuid.uuid4())
        blob_id = str(uuid.uuid4())

        # Save the file to S3
        filename = secure_filename(file.filename)
        self.storage_delegate.save_to_s3(file, filename)

        # Save the metadata to SQLite database
        song_data = self.metadata_delegate.save_to_db(container_id, blob_id, metadata, is_stem)

        return song_data

    def get_song_data(self, blob_id):
        return self.metadata_delegate.get_song_data(blob_id)

    def get_all_metadata(self):
        return self.metadata_delegate.list_all_songs()

    def list_songs_by_artist(self, artist_name):
        return self.metadata_delegate.list_songs_by_artist(artist_name)

    def list_all_songs(self):
        return self.metadata_delegate.list_all_songs()

    def search_all(self, search_term):
        return self.metadata_delegate.search_by_song_or_artist_name(search_term)


    def get_song_chunks(self, blob_id):
        return tt.chunkify()
