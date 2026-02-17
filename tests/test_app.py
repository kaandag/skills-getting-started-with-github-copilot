from fastapi.testclient import TestClient

from src import app

client = TestClient(app.app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # should be a dict with at least one known activity
    assert "Basketball" in data
    assert isinstance(data["Basketball"], dict)


def test_signup_and_duplicate():
    email = "testuser@mergington.edu"
    # ensure not signed up yet
    resp = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # duplicate signup returns 400
    resp2 = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant():
    email = "toremove@mergington.edu"
    # sign up first
    r1 = client.post(f"/activities/Tennis/signup?email={email}")
    assert r1.status_code == 200

    # now remove
    r2 = client.delete(f"/activities/Tennis/participants?email={email}")
    assert r2.status_code == 200
    assert "Removed" in r2.json().get("message", "")

    # removing again should 404
    r3 = client.delete(f"/activities/Tennis/participants?email={email}")
    assert r3.status_code == 404


def test_signup_nonexistent_activity():
    r = client.post(f"/activities/NoSuch/signup?email=foo@bar.com")
    assert r.status_code == 404


def test_remove_nonexistent_activity():
    r = client.delete(f"/activities/NoSuch/participants?email=foo@bar.com")
    assert r.status_code == 404
