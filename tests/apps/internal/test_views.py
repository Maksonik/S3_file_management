import pytest


@pytest.mark.vcr
async def test_get_healthcheck(test_client):
    response = test_client.get("/v1/healthcheck")
    assert response.json() == {"status": "ok", "App name": "S3 File Management"}
