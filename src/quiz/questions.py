import json
import random
from pathlib import Path
from pprint import PrettyPrinter
from typing import List, Dict
from pydantic.types import PositiveInt


def _load_song_data() -> Dict:
    file_path = Path(__file__)
    path = file_path / "../../resources/song_data.json"
    with open(path.resolve(), 'r') as file:
        return json.load(file)['songs']


def get_random_song(number_of_songs: PositiveInt) -> List[Dict]:
    """
    Returns a list of random songs' data from the song data JSON file.
    :return: Dictionary of song data
    """

    def yield_song(limit: PositiveInt):
        for i in range(limit):
            idx = random.randint(0, len(song_data) - 1)
            yield song_data[idx]

    song_data = _load_song_data()
    return [song for song in yield_song(number_of_songs)]


def get_song_by_id(song_id: int) -> Dict:
    song_data = _load_song_data()
    for song in song_data:
        if song["song_id"] == song_id:
            return song
    return {}


if __name__ == '__main__':
    printer = PrettyPrinter()
    printer.pprint(get_song_by_id(13003))
