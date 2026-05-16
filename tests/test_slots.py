async def test_get_slots_empty(client):
    response = await client.get("/slots/")
    assert response.status_code == 200
    assert response.json() == []

async def test_create_slot_as_specialist(client):
    await client.post("/auth/register", json={"name": "Test", "email": "test6@test.com", "password": "123456", "role": "specialist"})
    token = (await client.post("/auth/login", json={"username": "test6@test.com", "password": "123456"})).json()["access_token"]
    response = await client.post("/slots/", headers = {"Authorization": f"Bearer {token}"}, json = {"specialist_id": 1, "date": "2026-06-01", "time": "10:00:00"})
    assert response.status_code == 200
