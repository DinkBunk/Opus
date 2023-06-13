class StemDelegate:
    def __init__(self, db):
        self.db = db

    def create_stem(self, stem_id, artist, title, instrument, mix_id, blob_id):
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO stems (stem_id, artist, title, instrument, mix_id, blob_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (stem_id, artist, title, instrument, mix_id, blob_id)
            )
        self.db.commit()

    def get_stem(self, stem_id):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM stems WHERE stem_id = %s",
                (stem_id,)
            )
            return cursor.fetchone()

    def update_stem(self, stem_id, artist=None, title=None, instrument=None, mix_id=None, blob_id=None):
        with self.db.cursor() as cursor:
            cursor.execute(
                "UPDATE stems SET artist = %s, title = %s, instrument = %s, mix_id = %s, blob_id = %s WHERE stem_id = %s",
                (artist, title, instrument, mix_id, blob_id, stem_id)
            )
        self.db.commit()

    def search_by_artist_or_title(self, search_term):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM stems WHERE artist ILIKE %s OR title ILIKE %s",
                (search_term, search_term)
            )
            return cursor.fetchall()

    def get_all_stems(self):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM stems"
            )
            return cursor.fetchall()
