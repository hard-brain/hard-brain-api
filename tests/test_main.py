import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture
def song_data_schema():
    schema = {
        "song_id": 30000,
        "filename": "30000.mp3",
        "title": "B.O.D.Y.",
        "alt_titles": [],
        "genre": "HARD BODY MUSIC",
        "artist": 'BEMANI Sound Team "L.E.D. Sota F."& Starbitz',
    }
    return schema


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hard Brain"}


def test_get_random_question(song_data_schema):
    response = client.get("/question")
    assert response.status_code == 200
    assert len(response.json()) == 1
    for key in response.json()[0]:
        assert key in song_data_schema


def test_get_multiple_questions():
    response = client.get("/question?number_of_songs=3")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_song_by_song_id_passes(song_data_schema):
    response = client.get("/song/30000")
    assert response.status_code == 200
    assert response.json() == song_data_schema


def test_get_song_by_song_id_fails():
    response = client.get("/song/573000")
    assert response.status_code == 404


def test_get_audio_by_song_passes():
    response = client.get("/audio/30000")
    assert response.status_code == 200


def test_get_audio_by_song_id_fails_invalid_id():
    response = client.get("/audio/99999")
    assert response.status_code == 404
