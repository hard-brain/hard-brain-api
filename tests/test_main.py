import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture
def song_data_schema():
    schema = {
        "song_id": 13003,
        "filename": "D.C.fish.mp3",
        "title": "D.C.fish",
        "alt_titles": [
            "DC fish"
        ],
        "genre": "TECHNO",
        "artist": "DJ MURASAME"
    }
    return schema


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hard Brain"}


def test_get_random_question(song_data_schema):
    response = client.get("/question")
    assert response.status_code == 200
    for key in response.json():
        assert key in song_data_schema


def test_get_song_by_song_id_passes(song_data_schema):
    response = client.get("/song/13003")
    assert response.status_code == 200
    assert response.json() == song_data_schema


def test_get_song_by_song_id_fails():
    response = client.get("/song/573000")
    assert response.status_code == 404
