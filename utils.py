import base64
import hashlib
import hmac

from config import settings


def compute_secret_hash(username: str) -> str:
    message = username + settings.COGNITO_CLIENT_ID
    dig = hmac.new(
        settings.COGNITO_CLIENT_SECRET.encode("UTF-8"),
        msg=message.encode("UTF-8"),
        digestmod=hashlib.sha256,
    ).digest()

    return base64.b64encode(dig).decode()
