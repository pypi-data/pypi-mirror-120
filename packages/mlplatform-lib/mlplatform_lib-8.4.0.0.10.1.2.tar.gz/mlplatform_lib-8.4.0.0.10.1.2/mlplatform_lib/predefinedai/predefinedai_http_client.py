from mlplatform_lib.mlplatform.mlplatform_http_client import (
    MlPlatformHttpClient,
    MlPlatformUserAuth,
    MlPlatformRequestType,
)
from mlplatform_lib.dataclass.model.model_predefinedai_dto import ModelPredefinedaiDto
from typing import List
from mlplatform_lib.utils.dataclass_utils import to_dict, from_dict


class PredefinedAIHttpClient(MlPlatformHttpClient):
    def __init__(self, mlplatform_addr):
        super().__init__(mlplatform_addr=mlplatform_addr)

    def get_models(
        self, experiment_id: int, train_id: int, auth: MlPlatformUserAuth
    ) -> List[ModelPredefinedaiDto]:
        res = self.send_request(
            "models",
            {"experiments": experiment_id, "trains": train_id},
            {},
            {},
            auth,
            MlPlatformRequestType.READ,
        )
        model_infos = []
        for model_info in res.data:
            model_infos.append(from_dict(ModelPredefinedaiDto, model_info))
        return model_infos

    def insert_model(
        self, experiment_id: int, train_id: int, model: ModelPredefinedaiDto, auth: MlPlatformUserAuth
    ) -> ModelPredefinedaiDto:
        res = self.send_request(
            "models",
            {"experiments": experiment_id, "trains": train_id},
            {},
            to_dict(model),
            auth,
            MlPlatformRequestType.CREATE,
        )
        return from_dict(ModelPredefinedaiDto, res.data)
