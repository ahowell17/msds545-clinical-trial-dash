import io
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_login_and_upload(async_client):
    # Login
    res = await async_client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == status.HTTP_200_OK
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # CSV content
    csv_content = (
        "subject_id,age,gender,treatment_arm,site,visit_date\n"
        "S1,45,Female,Drug,SiteA,2025-01-01\n"
        "S2,50,Male,Placebo,SiteB,2025-01-02\n"
    )
    files = {
        "file": ("test.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    }

    res2 = await async_client.post("/upload/csv", headers=headers, files=files)
    assert res2.status_code == status.HTTP_200_OK
    body = res2.json()
    assert body["records_created"] == 2

    res3 = await async_client.get("/data/demographics", headers=headers)
    assert res3.status_code == status.HTTP_200_OK
    summary = res3.json()
    assert "by_gender" in summary
    assert "by_treatment_arm" in summary

