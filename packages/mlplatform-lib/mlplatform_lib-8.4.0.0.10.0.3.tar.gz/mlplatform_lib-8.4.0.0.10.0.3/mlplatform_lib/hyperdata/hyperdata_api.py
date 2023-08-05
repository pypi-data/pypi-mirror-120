from typing import List
from mlplatform_lib.api_client import ApiClient, RunMode
from mlplatform_lib.dataclass import (
    ColumnOfTableFromDefaultSource,
    TableFromDefaultDataSourceInfo, DataObject,
    DataObjectOutCol,
    DataObjectInfoList
)
from mlplatform_lib.hyperdata.hyperdata_http_client import HyperdataHttpClient, HyperdataUserAuth
from mlplatform_lib.hyperdata.hyperdata_local_checker import HyperdataLocalChecker
import os
import pathlib
import pandas as pd


class HyperdataApi:
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        if self.api_client.run_mode == RunMode.LOCAL:
            self.local_checker = HyperdataLocalChecker(api_client=api_client)
            self.local_checker.run()
            self.api_client.projectId = self.local_checker.project_id
            self.api_client.userId = self.api_client.user_id
            self.api_client.Authorization = self.local_checker.access_token

        self.hyperdata_client = HyperdataHttpClient(hd_addr=self.api_client.hyperdata_addr)
        self.hyperdata_auth = HyperdataUserAuth(
            project_id=self.api_client.projectId,
            user_id=self.api_client.userId,
            authorization=self.api_client.Authorization,
        )

    def download_csv(self, do_id: int, data_rootpath: str) -> str:
        result, sep, line_delim = self.hyperdata_client.download_do_to_csv(self.hyperdata_auth, do_id)

        pathlib.Path(data_rootpath).mkdir(parents=True, exist_ok=True)
        csv_path = os.path.join(data_rootpath, "%d.csv" % int(do_id))

        csv_str = result.data.decode("utf-8")
        if line_delim != "\n":
            csv_str.replace(line_delim, "\n")
        with open(csv_path, "w") as f:
            f.write(csv_str)

        if sep != ",":
            data = pd.read_csv(csv_path, sep=sep)
            data.to_csv(csv_path, sep=",", index=False)

        return csv_path

    def create_inference_result(self, table_name: str, object_name: str, columns: List[str]) -> int:
        default_datasource_id = self.hyperdata_client.get_default_datasource_id(auth=self.hyperdata_auth)
        self.hyperdata_client.create_dataobject_table(
            auth=self.hyperdata_auth,
            datasource_id=default_datasource_id,
            table_from_default_data_source=TableFromDefaultDataSourceInfo(
                tableName=table_name,
                columnList=[
                    ColumnOfTableFromDefaultSource(
                        columnName=column,
                        type="VARCHAR"
                    ) for column in columns
                ]
            )
        )
        self.hyperdata_client.create_dataobjects(
            auth=self.hyperdata_auth,
            datasource_id=default_datasource_id,
            dataobjects=DataObjectInfoList(
                data_object_info_list=[
                    DataObject(
                        name=object_name,
                        source_table_name=table_name,
                        subtype="Inference Result",
                        outCols=[
                            DataObjectOutCol(
                                name=column
                            ) for column in columns
                        ]
                    )
                ]
            )
        )
