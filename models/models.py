from sqlalchemy import create_engine, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base(metadata=MetaData(schema="opus_test")) # Here is where you specify the schema

class Stem(Base):
    __tablename__ = 'stems'
    stem_id = Column(String(50), primary_key=True)
    artist = Column(String(50))
    title = Column(String(50))
    instrument = Column(String(50))
    mix_id = Column(String(100))
    blob_id = Column(String(100))

class Mix(Base):
    __tablename__ = 'mixes'
    mix_id = Column(String(50), primary_key=True)
    artist = Column(String(50))
    title = Column(String(50))
    blob_id = Column(String(100))

    # one-to-many relationship with stems, string array of stem ids
    stem_ids = Column(String(100))

engine = create_engine('postgresql://postgres:5p4c3p471@localhost:5432/opusdb')

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)  # Creates the table

# Use a session to insert a new record
session = Session()
new_stem = Stem(stem_id=str(uuid.uuid4()), artist="Artist Name", title="Song Title", instrument="Instrument Name", mix_id="Mix ID", blob_id="Blob ID")
session.add(new_stem)
session.commit()

# Query the data
stems = session.query(Stem).all()
for stem in stems:
    print(stem.stem_id, stem.artist, stem.title)

session.close()