from app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health_returns_ok():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_info_has_expected_fields():
    data = client().get("/api/info").get_json()
    for field in ("hostname", "version", "environment", "uptime_seconds"):
        assert field in data


def test_index_page_renders():
    response = client().get("/")
    assert response.status_code == 200
    assert b"Home Lab Status" in response.data
