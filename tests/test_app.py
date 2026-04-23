import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities

# Original activities data for resetting
original_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team training and competitive matches for soccer players",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "lily@mergington.edu"]
    },
    "Basketball Training": {
        "description": "Skill development and scrimmages for basketball enthusiasts",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["nate@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media art projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["sara@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and stage productions for aspiring performers",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["hannah@mergington.edu", "sam@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science exploration activities",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabel@mergington.edu", "liam@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice debate skills and compete in speech tournaments",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["emma@mergington.edu", "jack@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the global activities dict before each test
    global activities
    activities.clear()
    activities.update(copy.deepcopy(original_activities))

@pytest.fixture
def client():
    # Create a TestClient for the FastAPI app
    with TestClient(app) as c:
        yield c

def test_get_activities(client):
    # Arrange: Client is set up via fixture

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response data
    assert response.status_code == 200
    assert response.json() == activities

def test_signup_valid(client):
    # Arrange: Choose an activity and a new email
    activity_name = "Chess Club"
    email = "new@student.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success and that email was added
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]

def test_signup_activity_not_found(client):
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Club"
    email = "test@student.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_signup_already_signed_up(client):
    # Arrange: Use an email already in the activity
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 400 error
    assert response.status_code == 400
    assert "Student is already signed up" in response.json()["detail"]

def test_remove_participant_valid(client):
    # Arrange: Choose an activity and an existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert: Check success and that email was removed
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

def test_remove_participant_activity_not_found(client):
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Club"
    email = "test@student.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert: Check 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_participant_not_found(client):
    # Arrange: Use an activity but non-existent participant
    activity_name = "Chess Club"
    email = "nonexistent@student.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert: Check 404 error
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]