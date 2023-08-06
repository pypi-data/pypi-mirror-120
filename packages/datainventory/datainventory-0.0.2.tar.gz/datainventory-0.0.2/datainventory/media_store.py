# Copyright © 2021 by IoT Spectator. All rights reserved.

"""Store for multimedia data such as video, audio, and image."""

import enum
import pathlib
import shutil
import sqlalchemy

from datetime import datetime
from datetime import timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from datainventory import _internal_store
from datainventory import common


class MediaType(enum.Enum):
    """Supporte media type."""

    Audio = enum.auto()
    Image = enum.auto()
    Video = enum.auto()


class Media(common.Base):
    """Table definition for multimedia."""

    __tablename__ = "media"

    filename = sqlalchemy.Column(sqlalchemy.String)
    fullpath = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    media_type = sqlalchemy.Column(sqlalchemy.String)
    format = sqlalchemy.Column(sqlalchemy.String)
    device_id = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime)
    size = sqlalchemy.Column(sqlalchemy.Integer)
    duration = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        """Provie nice representation for the media type."""
        return (
            f"<Media(filename={self.filename}, fullpath={self.fullpath}, "
            f"media_type={self.media_type}, format={self.format}, "
            f"device_id={self.device_id}, created_at={self.created_at}, "
            f"size={self.size}, duration={self.duration})>"
        )


class MediaStore(_internal_store.InternalStore):
    """Media Store."""

    def __init__(
        self,
        create_key,
        device_id: str,
        session: Session,
        connection: sqlalchemy.engine.Connection,
        data_inventory: pathlib.Path,
    ) -> None:
        _internal_store.InternalStore.__init__(
            self, create_key=create_key, device_id=device_id
        )
        self._session = session
        Media.__table__.create(bind=connection, checkfirst=True)
        self._data_inventory = data_inventory
        if not self._data_inventory.exists():
            self._data_inventory.mkdir(parents=True)

    def insert_media(
        self, file_path: pathlib.Path, media_type: MediaType, copy: bool = True
    ) -> pathlib.Path:
        """Insert a media."""
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist!")

        # Use copy2 to preserve the file metadata.
        shutil.copy2(src=file_path, dst=self._data_inventory)
        if not copy:
            # If not copy, perform move operation, i.e., copy and then delete
            file_path.unlink()

        dest_file = self._data_inventory / pathlib.Path(file_path.name)
        stat = dest_file.stat()
        data = Media(
            filename=dest_file.name,
            fullpath=str(dest_file),
            media_type=media_type.name,
            format=dest_file.suffix,
            device_id=self._device_id,
            created_at=datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc),
            size=stat.st_size,
            duration=0,  # FIXME: get the duration info if it's an audio or a video.
        )
        self._session.add(data)
        self._session.commit()
        return dest_file

    def query_data(
        self, query_statement: Optional[sqlalchemy.sql.Select] = None
    ) -> List:
        """Retrieve the media data."""
        if query_statement:
            result = self._session.execute(query_statement)
        else:
            query_statement = sqlalchemy.select(Media)
            result = self._session.execute(query_statement)
        return result.all()
