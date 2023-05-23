import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(
    async_client: AsyncClient,
    test_data: dict,
):
    response = await async_client.post("/register", json=test_data["user_register"])
    assert response.status_code == 201
    assert response.json() == test_data["user_register_response"]


@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient,
    test_data: dict,
):
    response = await async_client.post("/login", data=test_data["user_login"])
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_logout(
    async_client: AsyncClient,
    test_data: dict,
):
    # Assuming you are storing your access token in the 'Authorization' header
    headers = {"Authorization": f"Bearer {test_data['access_token']}"}
    response = await async_client.post(
        "/logout",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Successfully logged out"}
