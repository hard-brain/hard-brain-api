import json
import random
from pathlib import Path
from typing import List, Dict

from pydantic.types import PositiveInt


def _load_song_data() -> Dict:
    file_path = Path(__file__)
    path = file_path / "../../resources/song_data.json"
    with open(path.resolve(), 'r', encoding="utf-8") as file:
        return json.load(file)['songs']


def get_random_song(number_of_songs: PositiveInt) -> List[Dict]:
    """
    Returns a list of random songs' data from the song data JSON file.
    :return: Dictionary of song data
    """
    song_data = _load_song_data()

    def yield_song(limit: PositiveInt):
        for i in range(limit):
            key = random.choice(list(song_data.keys()))
            yield song_data[key]

    return [song for song in yield_song(number_of_songs)]


def get_song_by_id(song_id: int) -> Dict:
    song_data = _load_song_data()
    id_string = str(song_id)
    if id_string in song_data.keys():
        return song_data[id_string]
    return {}
