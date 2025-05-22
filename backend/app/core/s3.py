from pickle import FRAME

import boto3
from fastapi import UploadFile
from uuid import UUID
import asyncio

from app.core.config import settings

class YandexS3:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION_NAME
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    async def upload_file(self, file: UploadFile, key: str) -> str:
        def _sync_upload():
            self.s3.upload_fileobj(
                file.file,
                self.bucket_name,
                key
            )
            return f"https://{self.bucket_name}.storage.yandexcloud.net/{key}"

        return await asyncio.to_thread(_sync_upload)

s3_client = YandexS3()