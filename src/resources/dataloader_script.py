import json

from src.db import models, crud
from src.db.database import SessionLocal

with open("song_data.json", encoding="utf-8") as file:
    song_json = json.load(file)
    song_dict = song_json["songs"].values()
    for song in song_dict:
        song_model = models.Song(
            song_id=song["song_id"],
            filename=song["filename"],
            title=song["title"],
            alt_titles=", ".join(song["alt_titles"]),
            genre=song["genre"],
            artist=song["artist"],
        )
        with SessionLocal() as db:
            crud.create_song(db, song)
