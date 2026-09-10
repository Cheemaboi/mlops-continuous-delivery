from app import APPLICATION_VERSION, MODEL_VERSION, app


def test_home():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health_includes_release_metadata():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["application_version"] == APPLICATION_VERSION
    assert data["model_version"] == MODEL_VERSION
    assert "git_commit" in data


def test_prediction_doubles_the_value():
    response = app.test_client().post("/predict", json={"value": 5})

    assert response.status_code == 200
    assert response.get_json()["prediction"] == 10


def test_prediction_rejects_invalid_input():
    response = app.test_client().post("/predict", json={"value": "not-a-number"})

    assert response.status_code == 400
