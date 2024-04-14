import random
from pathlib import Path
from typing import Set

from pydantic.types import PositiveInt

from src.db import crud
from src.db.database import SessionLocal

file_path = Path(__file__)
songs_dir = set([file.stem for file in Path(file_path / "../../resources/songs").resolve().iterdir()])


def _load_song_ids() -> Set:
    with SessionLocal() as db:
        return set(crud.get_all_song_ids(db))


def _check_song_exists(key: str) -> bool:
    """
    Check if there is a file with matching song id using the JSON keys.
    :param key: JSON key to match against files
    :return: True if there is a file named {key}.mp3
    """
    return key in songs_dir


def get_random_song(number_of_songs: PositiveInt):
    """
    Returns a list of random songs' data from the song data JSON file.
    :return: Dictionary of song data
    """
    song_data = _load_song_ids()

    def yield_song(limit: PositiveInt, max_retries=10):
        for i in range(limit):
            key = None
            retries = 0
            song_id = "None"

            while not key and retries < max_retries:
                song_id = random.choice(list(song_data))
                if _check_song_exists(song_id):
                    key = song_id
                retries += 1

            if not key:
                raise FileNotFoundError(f"Did not find a file matching id '{song_id}' after {max_retries} retries")

            with SessionLocal() as db:
                yield crud.get_song(db, song_id)

    return [song for song in yield_song(number_of_songs)]


def get_song_by_id(song_id: str):
    with SessionLocal() as db:
        yield crud.get_song(db, song_id)
