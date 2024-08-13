import requests
from fastapi import HTTPException
from app.core.config import settings

def get_presigned_url():
    print(f"S3 Presigned URL: {settings.s3_presigned_url}")
    full_url = f"{settings.aws_api_base_url}{settings.s3_presigned_url}"
    print(f"Requesting URL: {full_url}")

    presigned_url_response = requests.get(
        full_url
    )
    
    print(presigned_url_response.json())

    if presigned_url_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to obtain presigned URL")

    return presigned_url_response.json()

def upload_to_s3(presigned_url: str, file_path: str):
    with open(file_path, "rb") as buffer:
        upload_response = requests.put(presigned_url, data=buffer)

    if upload_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to upload video to S3")
