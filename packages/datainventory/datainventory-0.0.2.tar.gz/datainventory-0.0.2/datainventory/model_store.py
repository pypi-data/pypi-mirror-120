# Copyright © 2021 by IoT Spectator. All rights reserved.

"""Store for machine learning models."""

import sqlalchemy

from typing import Tuple

from sqlalchemy.orm import Session

from datainventory import _internal_store
from datainventory import common


class Model(common.Base):
    """The table definition of learning models."""

    __tablename__ = "model"

    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    version = sqlalchemy.Column(sqlalchemy.String)


class ModelStore(_internal_store.InternalStore):
    """Model Store."""

    def __init__(self, create_key, device_id: str, session: Session) -> None:
        _internal_store.InternalStore.__init__(
            self, create_key=create_key, device_id=device_id
        )
        self._session = session

    def get_model(self, name: str, version: str) -> Tuple:
        """Retrieve the model according to the name and version from database."""
        raise NotImplementedError("The function is not implemented.")
