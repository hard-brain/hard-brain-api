from pydantic import BaseModel


class SongBase(BaseModel):
    song_id: str
    filename: str
    title: str
    alt_titles: str | None
    genre: str
    artist: str


class SongCreate(SongBase):
    pass


class Song(SongBase):
    class Config:
        orm_mode = True
