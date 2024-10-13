import random
from pathlib import Path
from typing import List

from pydantic.types import PositiveInt

from src.db import crud
from src.db.database import SessionLocal
from src.db.models import Song

file_path = Path(__file__)
songs_dir = set(
    [
        file.stem
        for file in Path(file_path / "../../resources/songs").resolve().iterdir()
        if len(file.stem) == 5
    ]
)


def _load_song_ids(specific_versions: set[int] = None) -> List:
    PREVIOUS_VERSION = 32
    return_all_ids = specific_versions is None or len(specific_versions) == 0 or specific_versions == set(range(1, PREVIOUS_VERSION + 1))
    with SessionLocal() as db:
        if return_all_ids:
            return list(crud.get_all_song_ids(db))
        else:
            return list(crud.get_specific_song_ids(db, specific_versions))


def _check_song_exists(key: str) -> bool:
    """
    Check if there is a file with matching song id using the JSON keys.
    :param key: JSON key to match against files
    :return: True if there is a file named {key}.mp3
    """
    return key in songs_dir


def get_random_song(number_of_songs: PositiveInt, specific_versions: str):
    """
    Returns a list of random songs' data from the song data JSON file.
    If specific_versions is a string of comma-separated integers, return only songs from those versions
    :return: Dictionary of song data
    """
    if specific_versions:
        song_data = _load_song_ids(set(map(int, specific_versions.split(','))))
    else:
        song_data = _load_song_ids()

    def yield_song(limit: PositiveInt, max_retries=10):
        for _ in range(limit):
            key = None
            retries = 0
            song_id = "None"

            while not key and retries < max_retries:
                song_id = random.choice(song_data)
                if _check_song_exists(song_id):
                    key = song_id
                retries += 1

            if not key:
                raise FileNotFoundError(
                    f"Did not find a file matching id '{song_id}' after {max_retries} retries"
                )

            with SessionLocal() as db:
                yield crud.get_song(db, song_id)

    return [song for song in yield_song(number_of_songs)]


def get_song_by_id(song_id: str) -> Song:
    with SessionLocal() as db:
        return crud.get_song(db, song_id)
