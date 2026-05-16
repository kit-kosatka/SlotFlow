async def test_register_success(client):
    response = await client.post("/auth/register", json={"name": "Test", "email": "test1@test.com", "password": "123456", "role": "client"})
    assert response.status_code == 200
    assert response.json() == {"message": "Registered successfully"}

async def test_register_duplicate(client):
    await client.post("/auth/register", json={"name": "Test", "email": "test1@test.com", "password": "123456", "role": "client"})
    response = await client.post("/auth/register", json={"name": "Test", "email": "test1@test.com", "password": "123456", "role": "client"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

async def test_login_success(client):
    registration = await client.post("/auth/register", json={"name": "Test3", "email": "test3@test.com", "password": "123456", "role": "client"})
    response = await client.post("/auth/login", json={"username": "test3@test.com", "password": "123456"})
    assert response.status_code == 200
    assert "access_token" in response.json()
