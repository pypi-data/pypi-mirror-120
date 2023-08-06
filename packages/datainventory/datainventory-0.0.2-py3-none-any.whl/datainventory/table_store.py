# Copyright © 2021 by IoT Spectator. All rights reserved.

"""Store for structured data."""

import datetime
import sqlalchemy

import pandas as pd

from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from datainventory import _internal_store
from datainventory import common


class TableStore(_internal_store.InternalStore):
    """Table Store."""

    def __init__(
        self,
        create_key,
        device_id: str,
        metadata: sqlalchemy.MetaData,
        session: Session,
    ) -> None:
        _internal_store.InternalStore.__init__(
            self, create_key=create_key, device_id=device_id
        )
        self._session = session
        self._metadata = metadata

    def create_table(
        self, table_name: str, columns: Dict[str, common.ColumnType]
    ) -> None:
        """Create a table."""
        columns["device_id"] = common.ColumnType.String
        columns["timestamp"] = common.ColumnType.DateTime

        table = sqlalchemy.Table(
            table_name,
            self._metadata,
            *(
                sqlalchemy.Column(column_name, column_type.value)
                for column_name, column_type in columns.items()
            ),
        )
        table.create(checkfirst=True)

    def insert(self, table_name: str, values: List[Dict]) -> None:
        """Insert data."""
        for item in values:
            item["device_id"] = self._device_id
            item["timestamp"] = datetime.datetime.utcnow()

        table = self._metadata.tables[table_name]
        self._session.execute(table.insert().values(values))
        self._session.commit()

    def query_data(  # type: ignore
        self, table_name: str, range: Optional[common.Range] = None
    ) -> pd.DataFrame:
        """Query data from a given table within a time range."""
        table: sqlalchemy.Table = self._metadata.tables[table_name]

        if range:
            start, end = range.get_range()
            if end:
                results = (
                    self._session.query(table)
                    .filter(table.c.timestamp >= start, table.c.timestamp <= end)
                    .all()
                )
            else:
                results = (
                    self._session.query(table).filter(table.c.timestamp >= start).all()
                )
        else:
            results = self._session.query(table).all()
        return pd.DataFrame(results, columns=table.columns.keys())
