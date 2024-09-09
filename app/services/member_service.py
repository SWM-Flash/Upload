from app.core.config import settings
import httpx

API_BASE_URL = settings.api_base_url
MEMBER_PATCH_ENDPOINT = "/members"

async def patch_member(token: str, member_data: dict):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{API_BASE_URL}{MEMBER_PATCH_ENDPOINT}",
            json=member_data,
            headers=headers
        )
        response.raise_for_status()

    return response.json()
