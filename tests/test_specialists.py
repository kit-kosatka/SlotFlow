async def test_get_specialists_empty(client):
    response = await client.get("/specialists/")
    assert response.status_code == 200
    assert response.json() == []

async def test_create_specialist_as_admin(client):
    await client.post("/auth/register", json={"name": "Test", "email": "test5@test.com", "password": "123456", "role": "admin"})
    login = await client.post("/auth/login", json={"username": "test5@test.com", "password": "123456"})
    token = login.json()["access_token"]
    response = await client.post("/specialists/?user_id=1", headers={"Authorization": f"Bearer {token}"}, json={"specialty": "Массажист", "description": "Опыт 5 лет"})
    assert response.status_code == 200

