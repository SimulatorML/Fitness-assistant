import pytest


@pytest.mark.asyncio
async def test_root(client):
    """Test if the API root is accessible"""
    response = await client.get("/") 
    assert response.status_code == 200