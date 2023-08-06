from typing import Tuple, Any

from fastapi import Request, HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import get_authorization_scheme_param, OAuth2
from integration_tools.api import BaseCredentialMixin


class AuthFlow(OAuth2):
    async def __call__(self, request: Request) -> Tuple:
        token: str = request.headers.get("Authorization")
        platform_id: str = request.query_params.get('platform_id')
        scheme, param = get_authorization_scheme_param(token)
        if not token or scheme.lower() != "token" or not platform_id:
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Permission Denied",
                )
            else:
                return None
        return token, platform_id


AuthFlow()


class Auth(BaseCredentialMixin):
    pass


async def get_smart_auth(auth_params: tuple = Depends(AuthFlow())):
    auth = Auth()
    return await auth.get_user_info_async(*auth_params)


async def get_credential(model: Any, request: Request, _=Depends(get_smart_auth)) -> Any:  # type: ignore
    credential_id = request.query_params.get('platform_id')
    credential = await model.AQ.find_one(_id=credential_id)
    if not credential:
        HTTPException(
            status_code=403, detail="Invalid credential",
        )
    return credential
