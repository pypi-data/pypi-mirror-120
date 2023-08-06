import logging
import os
import time
from collections import OrderedDict
from typing import Dict, List, Optional, Union

import pandas as pd
import yaml
from pyrasgo.api.connection import Connection
from pyrasgo.api.error import APIError
from pyrasgo.schemas import DataType, FeaturesYML
from pyrasgo.schemas import data_source as schema
from pyrasgo.utils import naming
from tqdm import tqdm


class DataSource(Connection):
    """
    Stores a Rasgo DataSource
    """

    def __init__(self, api_object, **kwargs):
        super().__init__(**kwargs)
        self._fields = schema.DataSource(**api_object)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Source(id={self.id}, name={self.name}, sourceType={self.sourceType}, table={naming.make_fqtn(self.table, self.tableDatabase, self.tableSchema)})"

    def __getattr__(self, item):
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            self.refresh()
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

# ----------
# Properties
# ----------



# -------
# Methods
#--------
    def display_source_code(self):
        """
        Convenience function to display the sourceCode property
        """
        return self._fields.sourceCode

    def read_into_df(self,
                     filters: Optional[Dict[str, str]] = None,
                     limit: Optional[int] = None) -> pd.DataFrame:
        """
        Pull Source data from DataWarehouse into a pandas Dataframe
        """
        from pyrasgo.api.read import Read
        return Read().source_data(id=self.id, filters=filters, limit=limit)

    def rebuild_from_source_code(self):
        """
        Rebuild the Source using the source code
        """
        raise NotImplementedError()

    def refresh(self):
        """
        Updates the Soure's attributes from the API
        """
        self._fields = schema.DataSource(**self._get(f"/data-source/{self.id}", api_version=1).json())

    def rename(self, new_name: str):
        """
        Updates a DataSource's display name
        """
        print(f"Renaming DataSource {self.id} from {self.name} to {new_name}")
        source = schema.DataSourceUpdate(id=self.id, name=new_name)
        self._fields = schema.DataSource(**self._patch(f"/data-source/{self.id}",
                                                    api_version=1, _json=source.dict(exclude_unset=True, exclude_none=True)).json())

    def to_dict(self) -> dict:
        return FeaturesYML(
                name = self._fields.name,
                sourceTable = self._fields.dataTable.fqtn,
                dimensions = [{"columnName": d.columnName, "dataType": d.dataType, "granularity": d.granularity.name} for d in self._fields.dimensions],
                features = self._fields.features,
                sourceCode = self._fields.sourceCode,
                sourceType = self._fields.sourceType
        ).dict(exclude_unset=False, by_alias=True)

    def to_yml(self, file_name: str,
                     directory: str = None,
                     overwrite: bool = True
    ) -> str:
        if directory is None:
            directory = os.getcwd()

        if directory[-1] == "/":
            directory = directory[:-1]

        if file_name.split(".")[-1] not in ['yaml', 'yml']:
            file_name += ".yaml"

        if os.path.exists(f"{directory}/{file_name}") and overwrite:
            logging.warning(f"Overwriting existing file {file_name} in directory: {directory}")

        safe_dumper = yaml.SafeDumper
        safe_dumper.add_representer(DataType, lambda self, data: self.represent_str(str(data.value)))
        safe_dumper.add_representer(OrderedDict, lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items()))
        safe_dumper.ignore_aliases = lambda self, data: True

        with open(f"{directory}/{file_name}", "w") as _yaml:
            yaml.dump(data=OrderedDict(self.to_dict()), Dumper=safe_dumper, stream=_yaml)

    def execute_transform(
        self,
        transform_id: int = None,
        transform_name: str = None,
        dimensions: List[str] = None,
        new_source_name: str = None,
        arguments: Dict[str, str] = {},
        utilities: Optional[List] = None
    ):
        from pyrasgo.api import Get, Publish

        if not (transform_id or transform_name):
            raise ValueError(f"please identify the transform to be executed by either ID or name")

        elif transform_name and not transform_id:
            available_transforms = self.get.transforms()
            for transform in available_transforms.transforms:
                if transform.name == transform_name:
                    response = self.publish.execute_transform(
                        transform_id=transform.id,
                        dimensions=dimensions,
                        data_source_id=self._fields.id,
                        new_source_name=new_source_name,
                        arguments=arguments,
                        utilities=utilities
                    )

                    return(response)
            raise ValueError(f"Unable to find a transform matching name: {transform_name}")

        else:
            response = Publish().execute_transform(
                transform_id=transform_id,
                dimensions=dimensions,
                data_source_id=self._fields.id,
                new_source_name=new_source_name,
                arguments=arguments,
                utilities=utilities
            )
            return(response)

        raise NotImplementedError(f"Unable to execute transform")

    def _make_table_metadata(self):
        payload = self.dataTable
        metadata = {
            "database": payload.databaseName,
            "schema": payload.schemaName,
            "table": payload.tableName,
        }
        return metadata
