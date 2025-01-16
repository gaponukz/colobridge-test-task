from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from config import settings
from dependencies import cognito_client, postgres_connection, s3_client
from src.application import dto, interactors
from src.infrastructure.repository import PostgresTasksRepository
from src.infrastructure.text_repository import S3TasksTextRepository
from src.infrastructure.worker import CeleryTasksWorker
from utils import compute_secret_hash

app = FastAPI()
security = HTTPBearer()

worker = CeleryTasksWorker()
text_repo = S3TasksTextRepository(s3_client, settings.S3_BUCKET_NAME)
repo = PostgresTasksRepository(postgres_connection)


class SignInRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


def validate_access_token(token=Security(security)):
    try:
        unverified_header = jwt.get_unverified_header(token.credentials)
        kid = unverified_header.get("kid")

        key = next((k for k in settings.JWKS["keys"] if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token")

        decoded_token = jwt.decode(
            token.credentials,
            key,
            algorithms=["RS256"],
            audience=settings.COGNITO_CLIENT_ID,
            issuer=f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/{settings.COGNITO_USER_POOL_ID}",
        )

        return decoded_token

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/signin")
async def signin(request: SignInRequest):
    try:
        response = cognito_client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": request.email,
                "PASSWORD": request.password,
                "SECRET_HASH": compute_secret_hash(request.email),
            },
        )

    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    except cognito_client.exceptions.UserNotConfirmedException:
        raise HTTPException(status_code=401, detail="User not confirmed.")

    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
    }


@app.post("/refresh")
async def refresh(
    refresh_token_request: RefreshTokenRequest, user=Depends(validate_access_token)
):
    try:
        response = cognito_client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token_request.refresh_token,
                "SECRET_HASH": compute_secret_hash(user["username"]),
            },
        )
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    except cognito_client.exceptions.InvalidParameterException:
        raise HTTPException(status_code=400, detail="Invalid request parameters.")

    return {
        "access_token": response["AuthenticationResult"]["AccessToken"],
    }


@app.get("/tasks")
async def get_tasks(_=Depends(validate_access_token)):
    return interactors.get_tasks(repo, text_repo)


@app.post("/tasks")
async def add_task(task: dto.CreateTaskInputDTO, _=Depends(validate_access_token)):
    return interactors.create_task(task, repo=repo, worker=worker, text_repo=text_repo)
