from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_version(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "v1.2.3")
    monkeypatch.setenv("GIT_SHA", "abc1234")
    monkeypatch.setenv("APP_ENV", "test")

    client = app.test_client()
    response = client.get("/version")
    data = response.get_json()

    assert response.status_code == 200
    assert data["version"] == "v1.2.3"
    assert data["commit"] == "abc1234"
    assert data["environment"] == "test"
