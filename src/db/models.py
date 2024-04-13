from sqlalchemy import String, Column

from src.db.database import Base


class Song(Base):
    __tablename__ = "song_data"

    song_id = Column(String, primary_key=True)
    filename = Column(String)
    title = Column(String)
    alt_titles = Column(String)
    genre = Column(String)
    artist = Column(String)
