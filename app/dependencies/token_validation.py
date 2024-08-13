from fastapi import Header, HTTPException, Depends
import requests
from app.core.config import settings

async def validate_token(accessToken: str = Header(...)):
    """Validate the user's token with an external API."""
    response = requests.post(
        f"{settings.api_base_url}{settings.token_validation_url}",
        headers={"Authorization": f"Bearer {accessToken}"}
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    return response.json()
