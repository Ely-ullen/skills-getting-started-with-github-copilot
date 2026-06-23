"""Backend tests for the Mergington High School FastAPI app."""


def test_get_activities(client):
    # Arrange
    # No setup is required because app startup loads initial activity data.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities").json()
    assert email in activities_response[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response.status_code == 200

    # Act
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"

    activities_response = client.get("/activities").json()
    assert activities_response[activity_name]["participants"].count(email) == 1


def test_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "remove_me@mergington.edu"
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response.status_code == 200

    # Act
    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities").json()
    assert email not in activities_response[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    delete_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Participant not found"
