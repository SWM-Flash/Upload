from fastapi import Header, HTTPException, Depends
import requests
from app.core.config import settings

async def validate_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization format.")
    
    token = authorization[len("Bearer "):]
    validation_url = f"{settings.api_base_url}{settings.token_validation_url}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(validation_url, headers=headers)
    
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized")
    elif response.status_code != 200:
        raise HTTPException(status_code=500, detail="Token validation failed")
    
    return token
