from fastapi import FastAPI, HTTPException
from pydantic import PositiveInt

from src.quiz.questions import get_random_song, get_song_by_id

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hard Brain"}


@app.get("/question")
def get_random_question(number_of_songs: PositiveInt = 1):
    return get_random_song(number_of_songs)


@app.get("/song/{song_id}")
def get_song_by_song_id(song_id: int):
    song_data = get_song_by_id(song_id)
    if len(song_data) == 0:
        raise HTTPException(status_code=404, detail="No song found with this ID")
    return song_data
