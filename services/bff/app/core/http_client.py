import httpx
from app.core.exceptions.service_exceptions import MicroserviceUnavailableError, MicroserviceError

async def http_request(method: str, url: str, token: str | None = None, json=None):

    headers = {}
    if token:
        headers["Authorization"] = token

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.request(method, url, json=json, headers=headers)
    except httpx.RequestError:
        raise MicroserviceUnavailableError(f"Service unreachable: {url}")

    if response.status_code >= 400:
        try:
            detail = response.json().get("error")
        except:
            detail = response.text

        raise MicroserviceError(response.status_code, detail)

    return response.json()
