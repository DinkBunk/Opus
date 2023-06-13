import psycopg2


class MixDelegate:
    def __init__(self, db):
        self.db = db

    def create_mix(self, mix_id, artist, title, stem_ids=None):
        if stem_ids is None:
            stem_ids = []
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO mixes (mix_id, artist, title, stem_ids) VALUES (%s, %s, %s, %s)",
                (mix_id, artist, title, stem_ids)
            )
        self.db.commit()

    def get_mix(self, mix_id):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM mixes WHERE mix_id = %s",
                (mix_id,)
            )
            return cursor.fetchone()

    def update_mix(self, mix_id, artist=None, title=None, blob_id=None):
        with self.db.cursor() as cursor:
            cursor.execute(
                "UPDATE mixes SET artist = %s, title = %s, blob_id = %s WHERE mix_id = %s",
                (artist, title, blob_id, mix_id)
            )
        self.db.commit()

    def add_stem_to_mix(self, mix_id, stem_id):
        with self.db.cursor() as cursor:
            cursor.execute(
                "UPDATE mixes SET stem_ids = array_append(stem_ids, %s) WHERE mix_id = %s",
                (stem_id, mix_id)
            )
        self.db.commit()
    def search_by_artist_or_title(self, search_term):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM mixes WHERE artist ILIKE %s OR title ILIKE %s",
                (search_term, search_term)
            )
            return cursor.fetchall()

    def get_stems_for_mix(self, mix_id):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT stem_ids FROM mixes WHERE mix_id = %s",
                (mix_id,)
            )
            return cursor.fetchone()

    def get_all_mixes(self):
        with self.db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM mixes"
            )
            return cursor.fetchall()