import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_health(async_client):
    res = await async_client.get("/health")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"status": "ok"}
