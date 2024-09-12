import json
from app.schemas.schemas import AuthRequest, AuthResponse


class AuthProcess:
    def __init__(self, response: str):
        self.response = response
        self.json_response = json.loads(response)

    def authenticate(self) -> AuthRequest:
        if 'detail' in self.json_response.keys():
            return self.process_error(self.json_response.get('detail'))

        is_auth = self.json_response.get('success', False)
        user_id = self.json_response.get('user_id', None)

        if not is_auth:
            return self.process_error(self, 'Permission denied')

        return AuthRequest(success=is_auth, user_id=user_id)

    def process_error(self, detail: str):
        return AuthRequest(success=False, user_id=None, detail=detail)