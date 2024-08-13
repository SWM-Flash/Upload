import requests
from fastapi import HTTPException
from app.core.config import settings

def trigger_transcode_job(s3_filename: str, accessToken: str):
    transcode_response = requests.post(
        f"{settings.api_base_url}{settings.transcode_url}",
        json={"filename": s3_filename},
        headers={"Authorization": f"Bearer {accessToken}"}
    )

    if transcode_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to trigger transcode job")

    return transcode_response.json()
