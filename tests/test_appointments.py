
async def test_create_appointment(client):
    await client.post("/auth/register", json={"name": "Test", "email": "test1@test.com", "password": "123456", "role": "specialist"})
    specialist_token = (await client.post("/auth/login", json={"username": "test1@test.com", "password": "123456"})).json()["access_token"]
    await client.post("/slots/", headers={"Authorization": f"Bearer {specialist_token}"}, json={"specialist_id": 1, "date": "2026-06-01", "time": "10:00:00"})
    await client.post("/auth/register", json={"name": "Client", "email": "test2@test.com", "password": "123456", "role": "client"})
    client_token = (await client.post("/auth/login", json={"username": "test2@test.com", "password": "123456"})).json()["access_token"]
    response = await client.post("/appointments/", headers={"Authorization": f"Bearer {client_token}"}, json={"slot_id": 1})
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


async def test_create_appointment_already_booked(client):
    await client.post("/auth/register", json={"name": "Test", "email": "test1@test.com", "password": "123456", "role": "specialist"})
    specialist_token = (await client.post("/auth/login", json={"username": "test1@test.com", "password": "123456"})).json()["access_token"]
    await client.post("/slots/", headers={"Authorization": f"Bearer {specialist_token}"}, json={"specialist_id": 1, "date": "2026-06-01", "time": "10:00:00"})
    await client.post("/auth/register", json={"name": "Client", "email": "test2@test.com", "password": "123456", "role": "client"})
    client_token = (await client.post("/auth/login", json={"username": "test2@test.com", "password": "123456"})).json()["access_token"]
    await client.post("/appointments/", headers={"Authorization": f"Bearer {client_token}"}, json={"slot_id": 1})
    response = await client.post("/appointments/", headers={"Authorization": f"Bearer {client_token}"}, json={"slot_id": 1})
    assert response.status_code == 400


