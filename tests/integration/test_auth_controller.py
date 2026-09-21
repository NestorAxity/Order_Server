from fastapi.testclient import TestClient

from order_server.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_register_and_login_e2e_flow() -> None:
    # 1. Probar registro vía HTTP
    register_payload = {
        "email": "e2e_user@example.com",
        "password": "e2e_password123",
        "full_name": "E2E User",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    print("STATUS:", register_response.status_code)
    print("BODY:", register_response.json())
    assert register_response.status_code == 201
    registered_data = register_response.json()
    assert registered_data["email"] == "e2e_user@example.com"
    assert "id" in registered_data

    # 2. Probar login vía HTTP (OAuth2 Form Data)
    login_payload = {
        "username": "e2e_user@example.com",
        "password": "e2e_password123",
    }
    login_response = client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
