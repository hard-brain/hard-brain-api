import re

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.db import models


def create_song(db: Session, song: models.Song):
    try:
        alt_titles = ", ".join(song["alt_titles"])
        db_song = models.Song(
            song_id=song["song_id"],
            filename=song["filename"],
            title=song["title"],
            alt_titles=alt_titles,
            genre=song["genre"],
            artist=song["artist"],
            game_version=song["game_version"],
        )
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
        return db_song
    except SQLAlchemyError as error:
        db.rollback()
        print(f"Error while adding song: {error}")


# noinspection PyTypeChecker
def get_song(db: Session, song_id: str):
    return db.query(models.Song).filter(models.Song.song_id == song_id).first()


def get_all_song_ids(db: Session):
    song_id_pattern = re.compile(r"([0-9]{5})")
    all_song_ids = list(db.query(models.Song.song_id).all())
    return [song_id_pattern.search(str(song)).group(1) for song in all_song_ids]


def get_specific_song_ids(db: Session, specific_versions: set[int] = None):
    song_id_pattern = re.compile(r"([0-9]{5})")
    all_song_ids = list(db.query(models.Song.song_id).filter(models.Song.game_version.in_(specific_versions)).all())
    return [song_id_pattern.search(str(song)).group(1) for song in all_song_ids]


# noinspection PyTypeChecker
def get_song_by_filename(db: Session, filename: str):
    return db.query(models.Song).filter(models.Song.filename == filename).first()


# noinspection PyTypeChecker
def get_song_by_game_version(db: Session, version: int):
    version_str = str(version).zfill(2)

    return (
        db.query(models.Song).filter(models.Song.song_id.startswith(version_str)).all()
    )
