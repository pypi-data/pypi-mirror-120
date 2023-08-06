# Copyright © 2021 by IoT Spectator. All rights reserved.

"""The main module of Data Inventory."""

import pathlib
import shutil
import sqlalchemy
import tarfile

import pandas as pd

from sqlalchemy.orm import sessionmaker

from datainventory import _internal_store
from datainventory import model_store
from datainventory import media_store
from datainventory import table_store


class Inventory:
    """Data Inventory."""

    def __init__(self, device_id: str, inventory: pathlib.Path) -> None:
        self._device_id = device_id
        self._inventory = inventory
        self._data_inventory = self._inventory / pathlib.Path("data")
        self._database_name = f"{self._inventory.name}.db"
        self._database = self._inventory / self._database_name

        if not self._inventory.exists():
            self._inventory.mkdir()
        self._engine = sqlalchemy.create_engine(f"sqlite:///{self._database}")
        self._metadata = sqlalchemy.MetaData(bind=self._engine)

    def get_media_store(self) -> media_store.MediaStore:
        """Return an instance of the media store."""
        Session = sessionmaker(bind=self._engine)
        return media_store.MediaStore(
            create_key=_internal_store.CREATE_KEY,
            device_id=self._device_id,
            session=Session(),
            connection=self._engine.connect(),
            data_inventory=self._data_inventory,
        )

    def get_model_store(self) -> model_store.ModelStore:
        """Return an instance of the model store."""
        Session = sessionmaker(bind=self._engine)
        return model_store.ModelStore(
            create_key=_internal_store.CREATE_KEY,
            device_id=self._device_id,
            session=Session(),
        )

    def get_table_store(self) -> table_store.TableStore:
        """Return an instance of the table store."""
        Session = sessionmaker(bind=self._engine)
        return table_store.TableStore(
            create_key=_internal_store.CREATE_KEY,
            device_id=self._device_id,
            metadata=self._metadata,
            session=Session(),
        )

    def export(self, dest_filename: pathlib.Path) -> pathlib.Path:
        """Export the entire data inventory."""
        self._metadata.reflect(self._engine)
        session = sessionmaker(bind=self._engine)()
        tables = list()
        for table_name in self._metadata.tables:
            table = self._metadata.tables[table_name]
            table_csv = self._inventory / pathlib.Path(f"{table}.csv")
            pd.DataFrame(
                session.query(table).all(), columns=table.columns.keys()
            ).to_csv(path_or_buf=table_csv, index=False)
            tables.append(table_csv)

        archive_path = f"{dest_filename.name}.tar.gz"
        with tarfile.open(name=archive_path, mode="w:gz") as tarball:
            tarball.add(name=self._data_inventory)
            for table_csv_file in tables:
                tarball.add(name=table_csv_file)
                table_csv_file.unlink()
        return pathlib.Path(archive_path)

    def destroy(self) -> None:
        """Destory the entire data inventory."""
        if self._inventory:
            shutil.rmtree(self._inventory)
