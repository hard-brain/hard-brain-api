from sqlmodel import SQLModel, Field


class Song(SQLModel, table=True):
    song_id: str | None = Field(default=None, primary_key=True)
    filename: str
    title: str
    alt_titles: str | None = None
    genre: str
    artist: str
