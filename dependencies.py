import boto3
import psycopg2

from config import settings

cognito_client = boto3.client("cognito-idp", region_name=settings.COGNITO_REGION)

s3_client = boto3.client("s3", region_name=settings.COGNITO_REGION)

postgres_connection = psycopg2.connect(
    dbname=settings.POSTGRES_DBNAME,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
)
