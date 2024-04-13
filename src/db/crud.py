from sqlalchemy.orm import Session

from src.db import models


# noinspection PyTypeChecker
def get_song(db: Session, song_id: str):
    return db.query(models.Song).filter(models.Song.song_id == song_id).first()


# noinspection PyTypeChecker
def get_song_by_filename(db: Session, filename: str):
    return db.query(models.Song).filter(models.Song.filename == filename).first()


# noinspection PyTypeChecker
def get_song_by_game_version(db: Session, version: int):
    version_str = str(version).zfill(2)

    return db.query(models.Song).filter(models.Song.song_id.startswith(version_str)).all()


def get_random_songs(db: Session, number: int):
    raise NotImplementedError
