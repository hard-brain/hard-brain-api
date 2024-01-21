import io

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import PositiveInt
from pathlib import Path
from ffmpeg.asyncio import FFmpeg
import wave

from src.quiz.questions import get_random_song, get_song_by_id
from src.quiz.connection import ConnectionManager

# setup stuff
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


# @app.websocket("/ws_audio")
# async def stream_song(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             # receive song id from the websocket and return appropriate audio stream
#             # song_id = await websocket.receive_text()
#             ffmpeg = (FFmpeg()
#                       .input("./resources/songs/TECHNOPHOBIA.mp3")
#                       .output("pipe:1", {"codec:a": "pcm_s16le"}, f='wav', vn=None))
#             wav_bytes = await ffmpeg.execute()
#             with wave.open(io.BytesIO(wav_bytes), 'rb') as wave_file:
#                 manager.send_personal_message()
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

async def audio_stream_generator(file_path: str):
    ffmpeg = (FFmpeg()
              .input(file_path)
              .output("pipe:1", {"codec:a": "pcm_s16le"}, f='wav', vn=None))
    wave_bytes = await ffmpeg.execute()
    with wave.open(io.BytesIO(wave_bytes), 'rb') as wave_file:
        yield wave_file.readframes(wave_file.getnframes())


@app.get("/audio")
async def stream_song():
    return StreamingResponse(audio_stream_generator("./resources/songs/TECHNOPHOBIA.mp3"))
