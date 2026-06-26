from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


def test_signup_adds_participant_to_activity():
    client = TestClient(app)

    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    payload = activities_response.json()
    assert email in payload[activity_name]["participants"]


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)

    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    payload = activities_response.json()
    assert email not in payload[activity_name]["participants"]
