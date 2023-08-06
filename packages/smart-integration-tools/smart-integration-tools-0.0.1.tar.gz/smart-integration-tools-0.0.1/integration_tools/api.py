import requests
import importlib
from typing import Union
from urllib.parse import unquote

from .settings import parse_tools_settings
from .exceptions import PermissionDenied

_, DEFAULT_URL, CREDENTIAL_MODEL, _ = parse_tools_settings()


class BaseAuthMixin(object):
    url = DEFAULT_URL

    def get_user_info(self, request_get_data: dict, headers: dict):
        if 'token' in request_get_data and "platform_id" in request_get_data:
            token = unquote(request_get_data["token"])
        elif 'HTTP_AUTHORIZATION' in headers and "platform_id" in request_get_data:
            token = headers["HTTP_AUTHORIZATION"]
        else:
            raise PermissionDenied(
                {"status": "error", "message": "you don't have permission to access"}
            )
        try:
            response = requests.get(
                f"{self.url}api/check-platform/?platform_id={request_get_data['platform_id']}",
                headers={"executetoken": token},
            )
        except requests.ConnectionError:
            raise PermissionDenied(
                {"status": "error", "message": "Authorization failed."}
            )

        if response.status_code != 200:
            raise PermissionDenied(
                {"status": "error", "message": "Authorization failed."}
            )

        return response.json()["auth_info"]

    def get_check_admin(self, request_get_data, *args, **kwargs):
        user_info = self.get_user_info(request_get_data, *args, **kwargs)
        user_id = user_info["id"]
        if user_id in (19, 22, 23, 55):
            return user_id
        raise PermissionDenied(
            {"status": "error", "message": "This endpoint only for smart admin users."}
        )


class BaseCredentialMixin(BaseAuthMixin):
    def get_object(self, credential_id: Union[int, str], platfrom_id: str):
        raise NotImplementedError()

    def get_credential(self, credential_id: Union[int, str], platfrom_id: str = 'prod'):
        return self.get_object(credential_id=credential_id, platfrom_id=platfrom_id)

    def get_credential_model(self):
        if CREDENTIAL_MODEL:
            module_path, model = CREDENTIAL_MODEL.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, model)
        raise AttributeError('miss CREDENTIAL_MODEL in settings')
