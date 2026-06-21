def test_register_and_login_user(client):
    payload = {"name": "Test Student", "email": "student@example.com", "password": "password123", "role": "student"}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "student@example.com"
    assert response.json()["role"] == "student"

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_get_profile_requires_token(client):
    # Each test gets a fresh DB; register the user first before logging in
    client.post(
        "/api/v1/auth/register",
        json={"name": "Test Student", "email": "student@example.com", "password": "password123", "role": "student"},
    )
    auth_data = {"username": "student@example.com", "password": "password123"}
    token_response = client.post("/api/v1/auth/login", data=auth_data)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    profile_response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == auth_data["username"]


def test_login_rate_limit(client):
    payload = {
        "name": "Rate Limit Student",
        "email": "rate-limit@example.com",
        "password": "password123",
        "role": "student",
    }
    register_response = client.post("/api/v1/auth/register", json=payload)
    assert register_response.status_code == 201

    status_codes = []
    for _ in range(40):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": payload["email"], "password": payload["password"]},
        )
        status_codes.append(response.status_code)
        if response.status_code == 429:
            break

    assert 429 in status_codes
