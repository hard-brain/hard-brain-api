import os
import pytest

from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(autouse=True)
def client():
    assert os.getenv("PGUSER")
    assert os.getenv("POSTGRES_PASSWORD")
    assert os.getenv("POSTGRES_DB")
    client = TestClient(app)
    return client


@pytest.fixture
def song_data_schema__30000():
    schema = {
        "song_id": "30000",
        "filename": "30000.mp3",
        "title": "B.O.D.Y.",
        "alt_titles": "",
        "genre": "HARD BODY MUSIC",
        "artist": 'BEMANI Sound Team "L.E.D. Sota F."& Starbitz',
        "game_version": 30
    }
    return schema


@pytest.fixture
def song_data_schema__07032():
    schema = {
        "song_id": "07032",
        "filename": "07032.mp3",
        "title": "Spica",
        "alt_titles": "",
        "genre": "HOUSE",
        "artist": "D.JW",
        "game_version": 7
    }
    return schema


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hard Brain"}


def test_get_song_by_song_id_passes__above_10000(client, song_data_schema__30000):
    response = client.get("/song/30000")
    assert response.status_code == 200
    assert response.json() == song_data_schema__30000


# todo: make parameterized test for passing cases
def test_get_song_by_song_id_passes__below_10000(client, song_data_schema__07032):
    response = client.get("/song/07032")
    assert response.status_code == 200
    assert response.json() == song_data_schema__07032


def test_get_song_by_song_id_fails(client):
    response = client.get("/song/573000")
    assert response.status_code == 404


def test_get_audio_by_song_id_fails_invalid_id(client):
    response = client.get("/audio/99999")
    assert response.status_code == 404


def test_get_question(client):
    response = client.get("/question")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_question_with_params(client):
    response = client.get(f"/question?number_of_songs=10&version_string=1,23,5,6,7")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json) == 10

    expected = set((1, 23, 5, 6 ,7))
    for actual in response_json:
        assert int(actual["game_version"]) in expected