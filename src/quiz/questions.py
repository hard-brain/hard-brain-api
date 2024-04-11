import json
import random
from pathlib import Path
from typing import List, Dict

from pydantic.types import PositiveInt

file_path = Path(__file__)
songs_dir = set([file.stem for file in Path(file_path / "../../resources/songs").resolve().iterdir()])


def _load_song_data() -> Dict:
    json_path = file_path / "../../resources/song_data.json"
    with open(json_path.resolve(), 'r', encoding="utf-8") as file:
        return json.load(file)['songs']


def _check_song_exists(key: str) -> bool:
    """
    Check if there is a file with matching song id using the JSON keys.
    :param key: JSON key to match against files
    :return: True if there is a file named {key}.mp3
    """
    return key in songs_dir


def get_random_song(number_of_songs: PositiveInt) -> List[Dict]:
    """
    Returns a list of random songs' data from the song data JSON file.
    :return: Dictionary of song data
    """
    song_data = _load_song_data()

    def yield_song(limit: PositiveInt, max_retries=10):
        for i in range(limit):
            key = None
            retries = 0
            song_id = "None"

            while not key and retries < max_retries:
                song_id = random.choice(list(song_data.keys()))
                if _check_song_exists(song_id):
                    key = song_id
                retries += 1

            if not key:
                raise FileNotFoundError(f"Did not find a file matching id '{song_id}' after {max_retries} retries")

            yield song_data[key]

    return [song for song in yield_song(number_of_songs)]


def get_song_by_id(song_id: str) -> Dict:
    song_data = _load_song_data()
    if song_id in song_data.keys():
        return song_data[song_id]
    return {}
