"""API tests: auth, authorisation (no access to other users' topics), validation, rate limiting, injection safety."""
import sqlite3, time
import jwt, pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app import security

PW = "correct horse battery"


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(str(tmp_path / "t.db"), login_limit=5, login_window=60))


def token(c, email="a@example.com"):
    c.post("/auth/register", json={"email": email, "password": PW})
    r = c.post("/auth/login", json={"email": email, "password": PW})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_register_login_and_crud(client):
    h = token(client)
    r = client.post("/topics", json={"title": "Two pointers", "category": "dsa"}, headers=h)
    assert r.status_code == 201 and r.json()["status"] == "todo"
    tid = r.json()["id"]
    assert client.patch(f"/topics/{tid}", json={"status": "done", "revised": True}, headers=h).json()["revisions"] == 1
    assert client.get("/topics?status=done", headers=h).json()[0]["id"] == tid
    assert client.get("/stats", headers=h).json()["dsa"]["done"] == 1
    assert client.delete(f"/topics/{tid}", headers=h).status_code == 204
    assert client.get("/topics", headers=h).json() == []


def test_duplicate_email_and_wrong_password(client):
    token(client)
    assert client.post("/auth/register", json={"email": "A@example.com", "password": PW}).status_code == 409
    r = client.post("/auth/login", json={"email": "a@example.com", "password": "wrong password!"})
    assert r.status_code == 401 and r.json()["detail"] == "Wrong email or password"
    assert client.post("/auth/login", json={"email": "nobody@example.com", "password": PW}).json()["detail"] == "Wrong email or password"


def test_requires_valid_token(client):
    assert client.get("/topics").status_code == 401
    assert client.get("/topics", headers={"Authorization": "Bearer not-a-token"}).status_code == 401
    forged = jwt.encode({"sub": "1", "exp": int(time.time()) + 600}, "x" * 32, algorithm="HS256")
    assert client.get("/topics", headers={"Authorization": f"Bearer {forged}"}).status_code == 401
    expired = jwt.encode({"sub": "1", "iat": 0, "exp": 1}, security.jwt_secret(), algorithm="HS256")
    assert client.get("/topics", headers={"Authorization": f"Bearer {expired}"}).status_code == 401
    none_alg = jwt.encode({"sub": "1", "exp": int(time.time()) + 600}, None, algorithm="none")
    assert client.get("/topics", headers={"Authorization": f"Bearer {none_alg}"}).status_code == 401


def test_users_cannot_touch_each_others_topics(client):
    a, b = token(client, "a@example.com"), token(client, "b@example.com")
    tid = client.post("/topics", json={"title": "A's topic", "category": "security"}, headers=a).json()["id"]
    assert client.get("/topics", headers=b).json() == []
    assert client.patch(f"/topics/{tid}", json={"status": "done"}, headers=b).status_code == 404
    assert client.delete(f"/topics/{tid}", headers=b).status_code == 404
    assert client.get("/topics", headers=a).json()[0]["status"] == "todo"


def test_validation(client):
    h = token(client)
    assert client.post("/topics", json={"title": "", "category": "dsa"}, headers=h).status_code == 422
    assert client.post("/topics", json={"title": "x" * 201, "category": "dsa"}, headers=h).status_code == 422
    assert client.post("/topics", json={"title": "ok", "category": "cooking"}, headers=h).status_code == 422
    assert client.post("/auth/register", json={"email": "not-an-email", "password": PW}).status_code == 422
    assert client.post("/auth/register", json={"email": "c@example.com", "password": "short"}).status_code == 422


def test_sql_injection_is_stored_as_text(client):
    h = token(client)
    evil = "x'); DROP TABLE topics; --"
    assert client.post("/topics", json={"title": evil, "category": "dsa"}, headers=h).status_code == 201
    assert client.get("/topics", headers=h).json()[0]["title"] == evil


def test_login_rate_limit(client):
    token(client)
    codes = [client.post("/auth/login", json={"email": "a@example.com", "password": "wrong password!"}).status_code for _ in range(6)]
    assert codes[:4] == [401] * 4 and codes[-1] == 429   # 1 login in token() + 4 failures = 5 allowed, then blocked


def test_passwords_are_hashed(client, tmp_path):
    token(client)
    stored = sqlite3.connect(tmp_path / "t.db").execute("SELECT password_hash FROM users").fetchone()[0]
    assert PW not in stored and stored.startswith("scrypt$")
    assert security.verify_password(PW, stored) and not security.verify_password("nope", stored)


def test_security_headers(client):
    r = client.get("/health")
    assert r.headers["X-Content-Type-Options"] == "nosniff" and r.headers["X-Frame-Options"] == "DENY"


def test_refuses_weak_secret(monkeypatch, tmp_path):
    monkeypatch.setenv("JWT_SECRET", "short")
    with pytest.raises(RuntimeError):
        create_app(str(tmp_path / "w.db"))
