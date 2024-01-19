import json
import random
from pathlib import Path
from pprint import PrettyPrinter


def _load_song_data() -> dict:
    file_path = Path(__file__)
    path = file_path / "../../resources/song_data.json"
    with open(path.resolve(), 'r') as file:
        return json.load(file)['songs']


def get_random_song() -> dict:
    """
    Returns a random song's data from the song data JSON file.
    :return: Dictionary of song data
    """
    song_data = _load_song_data()
    idx = random.randint(0, len(song_data) - 1)
    return song_data[idx]


def get_song_by_id(song_id: int) -> dict:
    song_data = _load_song_data()
    for song in song_data:
        if song["song_id"] == song_id:
            return song
    return {}


if __name__ == '__main__':
    printer = PrettyPrinter()
    printer.pprint(get_song_by_id(13003))
