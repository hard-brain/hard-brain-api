from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import PositiveInt

from src.quiz.questions import get_random_song, get_song_by_id

# setup stuff
app = FastAPI()
app_path = Path(f"{__file__}/..")


@app.get("/")
def read_root():
    return {"msg": "Hard Brain"}


@app.get("/question")
def get_random_question(number_of_songs: PositiveInt = 1):
    return get_random_song(number_of_songs)


@app.get("/song/{song_id}")
def get_song_data_by_id(song_id: str):
    song_data = get_song_by_id(song_id)
    if len(song_data) == 0:
        raise HTTPException(status_code=404, detail="No song found with this ID")
    return song_data


@app.get("/audio/{song_id}")
def get_song_audio_by_id(song_id: str):
    song_data = get_song_by_id(song_id)
    if len(song_data) == 0:
        raise HTTPException(status_code=404, detail="No song found with this ID")
    fp = app_path / f"resources/songs/{song_data['filename']}"
    if not fp.resolve().exists():
        raise HTTPException(
            status_code=404, detail="No song file found for this song ID"
        )
    return FileResponse(fp.resolve(), media_type="audio/mp3")
