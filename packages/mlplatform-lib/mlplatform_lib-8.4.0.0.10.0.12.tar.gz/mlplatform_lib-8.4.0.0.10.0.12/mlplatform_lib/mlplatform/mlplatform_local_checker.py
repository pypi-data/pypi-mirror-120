from mlplatform_lib.api_client import ApiClient
from mlplatform_lib.hyperdata.hyperdata_http_client import HyperdataHttpClient, HyperdataUserAuth
from mlplatform_lib.utils.print_utils import print_header


class MlPlatformLocalChecker:
    def __init__(self, api_client: ApiClient):
        self.train_do_name = api_client.train_do_name
        self.inference_do_name = api_client.inference_do_name
        self.hyperdata_client = HyperdataHttpClient(hd_addr=api_client.hyperdata_addr)
        self.hyperdata_user_auth = HyperdataUserAuth(
            project_id=api_client.projectId, user_id=api_client.userId, authorization=api_client.Authorization
        )

        # generated
        self.train_do_id = None
        self.inference_do_id = None

    """
    def _check_mlplatform_server_connect(self):
        self._print_header(f'check mlplatform server "{self.mlplatform_addr}" connection.')
        self.mlplatform_request_header = {
            "projectId": str(self.project_id),
            "Authorization": self.access_token,
            "userId": self.user_id,
            "authorizationType": "hyperdata",
            "Content-Type": "application/json",
        }
        res = requests.get(self.mlplatform_addr, headers=self.mlplatform_request_header)
        if res.status_code != 200:
            print(
                "cannot connect to %s. mlplatform server returns status code %d"
                % (self.mlplatform_addr, res.status_code)
            )
            raise Exception(res)
        print("check mlplatform server connection end.\n")
    """

    def _check_train_do_exist(self):
        print_header(f'check is train do "{self.train_do_name}" exist.')

        do_list = self.hyperdata_client.get_do_list(self.hyperdata_user_auth)
        for do_info in do_list:
            if do_info.name == self.train_do_name:
                self.train_do_id = do_info.id
                print("check train do end.\n")
                return

        print(f'cannot found train do "{self.train_do_name}".')
        exit(1)

    def _check_inference_do_exist(self):
        print_header(f'check is inference do "{self.inference_do_name}" exist.')
        do_list = self.hyperdata_client.get_do_list(self.hyperdata_user_auth)

        for do_info in do_list:
            if do_info.name == self.inference_do_name:
                print("check inference do end.\n")
                self.inference_do_id = do_info.id
                return

        print(f'cannot found inference do "{self.inference_do_name}".')
        exit(1)

    def run(self):
        self._check_train_do_exist()
        self._check_inference_do_exist()
