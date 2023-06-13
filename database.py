import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get('GOOGLE_SQL_USER')
DB_PASS = os.environ.get('GOOGLE_SQL_PASS')
DB_NAME = 'opus-db'
DB_HOST = '34.69.202.204'

# Create the connection string
connection_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

# Create the engine
engine = create_engine(connection_string)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()