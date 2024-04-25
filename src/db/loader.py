import json

from src.db import models, crud
from src.db.database import SessionLocal


def load_into_db(json_path: str):
    with open(json_path, encoding="utf-8") as file:
        song_json = json.load(file)
        song_dict = song_json["songs"].values()
        for song in song_dict:
            with SessionLocal() as db:
                crud.create_song(db, song)


def is_song_table_empty():
    with SessionLocal() as db:
        return len(crud.get_all_song_ids(db)) == 0
