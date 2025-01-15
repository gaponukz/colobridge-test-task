import uuid

from src.application.interfaces import TasksTextRepository


class S3TasksTextRepository(TasksTextRepository):
    def __init__(self, client, bucket_name: str):
        self._client = client
        self._bucket_name = bucket_name

    def load(self, text: str) -> str:
        file_name = f"{uuid.uuid4()}.txt"

        self._client.put_object(Bucket=self._bucket_name, Key=file_name, Body=text)

        return f"s3://{self._bucket_name}/{file_name}"

    def get(self, link: str) -> str:
        _, _, bucket, *key_parts = link.split("/")
        key = "/".join(key_parts)

        response = self._client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")

        return content
