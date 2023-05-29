import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


@pytest.mark.asyncio
async def test_register_user(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_data: dict,
):
    payload = test_data["case_register_user"]["payload"]
    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_register_user"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(User).where(User.uuid == got["uuid"])
    results = await async_session.execute(statement=statement)
    user = results.scalar_one()

    for k, v in want.items():
        assert getattr(user, k) == v


@pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_data: dict,
):
    user_data = test_data["initial_data"]["user"]
    statement = insert(User).values(user_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_data["case_login"]["payload"]
    response = await async_client.post("/auth/token", data=payload)

    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/users", headers=headers)

    assert response.status_code == 200

    got = response.json()
    want = test_data["case_login"]["want"]

    for k, v in want.items():
        assert got[k] == v


# @pytest.mark.asyncio
# async def test_logout(
#     async_client: AsyncClient,
#     async_session: AsyncSession,
#     test_data: dict,
# ):
#     headers = {"Authorization": f"Bearer {test_data['access_token']}"}
#     response = await async_client.post("/logout", headers=headers)

#     assert response.status_code == 200
#     assert response.json() == {"detail": "Successfully logged out"}
