from copy import deepcopy

import pytest

from src import app as backend


def test_root_redirects_to_frontend(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_list_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert set(activities) == {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Track and Field",
        "Art Club",
        "Drama Club",
        "Science Club",
        "Debate Club",
    }
    assert activities == backend.activities
    assert activities["Chess Club"] == {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    }
    for details in activities.values():
        assert set(details) == {
            "description", "schedule", "max_participants", "participants"
        }
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)
        assert all(isinstance(email, str) for email in details["participants"])


def test_signup_updates_activity(client):
    before = deepcopy(backend.activities)
    email = "new+student@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    expected = deepcopy(before)
    expected["Chess Club"]["participants"].append(email)
    assert backend.activities == expected
    updated = client.get("/activities")
    assert updated.status_code == 200
    assert updated.json() == expected
    assert updated.json()["Chess Club"]["participants"].count(email) == 1


def test_unregister_updates_activity(client):
    expected = deepcopy(backend.activities)
    email = expected["Chess Club"]["participants"][0]
    expected["Chess Club"]["participants"].remove(email)

    response = client.delete(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert backend.activities == expected
    updated = client.get("/activities")
    assert updated.status_code == 200
    assert updated.json() == expected


@pytest.mark.parametrize(
    "method, activity, email, status, detail",
    [
        (
            "POST", "Chess Club", "michael@mergington.edu", 400,
            "Student already signed up for this activity",
        ),
        (
            "POST", "Unknown Activity", "new@mergington.edu", 404,
            "Activity not found",
        ),
        (
            "DELETE", "Unknown Activity", "michael@mergington.edu", 404,
            "Activity not found",
        ),
        (
            "DELETE", "Chess Club", "new@mergington.edu", 404,
            "Student is not signed up for this activity",
        ),
    ],
)
def test_rejected_mutation_preserves_activities(
    client, method, activity, email, status, detail
):
    before = deepcopy(backend.activities)

    response = client.request(
        method, f"/activities/{activity}/signup", params={"email": email}
    )

    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert backend.activities == before


@pytest.mark.parametrize("method", ["POST", "DELETE"])
def test_email_is_required(client, method):
    before = deepcopy(backend.activities)

    response = client.request(method, "/activities/Chess Club/signup")

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"] and "missing" in error["type"]
        for error in response.json()["detail"]
    )
    assert backend.activities == before
