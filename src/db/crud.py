from sqlalchemy.orm import Session

from src.db import models, schemas


def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


# noinspection PyTypeChecker
def get_song(db: Session, song_id: str):
    return db.query(models.Song).filter(models.Song.song_id == song_id).first()


def get_all_song_ids(db: Session):
    return db.query(models.Song.song_id).all()


# noinspection PyTypeChecker
def get_song_by_filename(db: Session, filename: str):
    return db.query(models.Song).filter(models.Song.filename == filename).first()


# noinspection PyTypeChecker
def get_song_by_game_version(db: Session, version: int):
    version_str = str(version).zfill(2)

    return db.query(models.Song).filter(models.Song.song_id.startswith(version_str)).all()
