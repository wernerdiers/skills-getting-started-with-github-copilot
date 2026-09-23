from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants?email={email}")

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
