from models.models import Session, Stem


class MetadataDelegate:
    def __init__(self):
        self.db = Base

    def save_to_db(self, container_id, blob_id, metadata, is_stem):
        metadata_entry = Metadata(blob_id=blob_id,
                                  artist_name=metadata['artist_name'],
                                  song_name=metadata['song_name'],
                                  is_stem=is_stem)
        self.db.session.add(metadata_entry)
        self.db.session.commit()
        return metadata_entry.serialize()


    def search_by_song_or_artist_name(self, search_term):
        return Metadata.query.filter(
            Metadata.artist_name.contains(search_term) | Metadata.song_name.contains(search_term)).all()


    def list_all_songs(self):
        return Metadata.query.all()