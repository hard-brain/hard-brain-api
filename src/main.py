from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import PositiveInt
from pathlib import Path

from src.quiz.questions import get_random_song, get_song_by_id
from src.quiz.connection import ConnectionManager

app = FastAPI()
manager = ConnectionManager()
path = Path(__file__)
songs_dir_path = path / "../resources/songs"
app.mount("/resources/songs", StaticFiles(directory=songs_dir_path.resolve()), name="songs")


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


@app.websocket("/ws_audio/")
async def stream_song(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # receive song id from the websocket and return appropriate audio stream
            song_id = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
