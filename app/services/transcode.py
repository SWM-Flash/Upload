import requests
from fastapi import HTTPException
from app.core.config import settings

def trigger_transcode_job(request_data: dict):
    transcode_response = requests.post(
        f"{settings.aws_api_base_url}{settings.transcode_url}",
        json=request_data
    )
    
    print(transcode_response.json())

    if transcode_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to trigger transcode job")

    return transcode_response.json()
