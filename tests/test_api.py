from fastapi.testclient import TestClient
from api.app import get_application

# Create a test client
app = get_application()
client = TestClient(app)

def test_health_check():
    """Test if the API root is accessible"""
    response = client.get("/")
    assert response.status_code == 200  

