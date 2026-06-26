from uuid import uuid4


def test_get_activities_returns_activity_list(test_client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = test_client.get(endpoint)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_adds_participant_to_activity(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"
    signup_endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = test_client.post(
        signup_endpoint,
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = test_client.get("/activities")
    payload = activities_response.json()
    assert email in payload[activity_name]["participants"]


def test_signup_rejects_duplicate_registration(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"
    signup_endpoint = f"/activities/{activity_name}/signup"

    # Act
    first_response = test_client.post(
        signup_endpoint,
        params={"email": email},
    )
    second_response = test_client.post(
        signup_endpoint,
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"
    signup_endpoint = f"/activities/{activity_name}/signup"
    unregister_endpoint = f"/activities/{activity_name}/unregister"

    signup_response = test_client.post(
        signup_endpoint,
        params={"email": email},
    )
    assert signup_response.status_code == 200

    # Act
    unregister_response = test_client.delete(
        unregister_endpoint,
        params={"email": email},
    )

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = test_client.get("/activities")
    payload = activities_response.json()
    assert email not in payload[activity_name]["participants"]


def test_unregister_via_participant_path(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@example.com"
    signup_endpoint = f"/activities/{activity_name}/signup"
    delete_path = f"/activities/{activity_name}/participants/{email}"

    signup_response = test_client.post(
        signup_endpoint,
        params={"email": email},
    )
    assert signup_response.status_code == 200

    # Act
    path_response = test_client.delete(delete_path)

    # Assert
    assert path_response.status_code == 200
    assert path_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = test_client.get("/activities")
    payload = activities_response.json()
    assert email not in payload[activity_name]["participants"]
