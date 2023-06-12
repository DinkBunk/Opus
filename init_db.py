from sqlalchemy import create_engine
from models.models import Base  # import the Base from your models

engine = create_engine('sqlite:///opus.db')
Base.metadata.create_all(engine)