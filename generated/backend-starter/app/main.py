"""Study-tracker REST API: register, log in, and track study topics. Every topic query is scoped to the logged-in user.
Run: JWT_SECRET=... uvicorn app.main:app --reload   (docs at http://127.0.0.1:8000/docs)"""
import sqlite3
from enum import Enum
from typing import Optional

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from . import db
from .security import RateLimiter, create_token, decode_token, hash_password, jwt_secret, verify_password

try:  # EmailStr needs the optional email-validator package; fall back to a simple pattern check
    import email_validator  # noqa: F401
    Email = EmailStr
except ImportError:
    from typing import Annotated
    Email = Annotated[str, Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=254)]


class Category(str, Enum):
    dsa = "dsa"; core_cs = "core_cs"; security = "security"; cloud = "cloud"; ai = "ai"


class Status(str, Enum):
    todo = "todo"; doing = "doing"; done = "done"


class Credentials(BaseModel):
    email: Email
    password: str = Field(min_length=10, max_length=128)


class TopicIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: Category


class TopicPatch(BaseModel):
    status: Optional[Status] = None
    revised: bool = False


def create_app(db_path=None, login_limit=5, login_window=60):
    jwt_secret()  # fail at startup, not at first login, if the secret is missing or weak
    app = FastAPI(title="Study tracker API", version="0.1.0")
    conn = db.connect(db_path)
    limiter = RateLimiter(login_limit, login_window)
    bearer = HTTPBearer(auto_error=False)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    def current_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer)) -> int:
        if creds is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token", headers={"WWW-Authenticate": "Bearer"})
        try:
            return decode_token(creds.credentials)
        except jwt.PyJWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

    def own_topic(topic_id: int, user_id: int):
        row = conn.execute("SELECT * FROM topics WHERE id = ? AND user_id = ?", (topic_id, user_id)).fetchone()
        if row is None:  # 404 for both 'missing' and 'someone else's', so ids cannot be probed
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Topic not found")
        return row

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/auth/register", status_code=201)
    def register(body: Credentials):
        try:
            with conn:
                conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (body.email.lower(), hash_password(body.password)))
        except sqlite3.IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
        return {"message": "registered"}

    @app.post("/auth/login")
    def login(body: Credentials, request: Request):
        key = f"{request.client.host if request.client else 'unknown'}:{body.email.lower()}"
        if not limiter.allow(key):
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many login attempts, try again later")
        row = conn.execute("SELECT id, password_hash FROM users WHERE email = ?", (body.email.lower(),)).fetchone()
        if row is None or not verify_password(body.password, row["password_hash"]):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password")  # same message for both cases
        return {"access_token": create_token(row["id"]), "token_type": "bearer"}

    @app.get("/topics")
    def list_topics(user_id: int = Depends(current_user), status_: Optional[Status] = Query(None, alias="status")):
        q, args = "SELECT * FROM topics WHERE user_id = ?", [user_id]
        if status_:
            q += " AND status = ?"; args.append(status_.value)
        return [dict(r) for r in conn.execute(q + " ORDER BY id", args)]

    @app.post("/topics", status_code=201)
    def add_topic(body: TopicIn, user_id: int = Depends(current_user)):
        with conn:
            cur = conn.execute("INSERT INTO topics (user_id, title, category) VALUES (?, ?, ?)", (user_id, body.title, body.category.value))
        return dict(own_topic(cur.lastrowid, user_id))

    @app.patch("/topics/{topic_id}")
    def update_topic(topic_id: int, body: TopicPatch, user_id: int = Depends(current_user)):
        own_topic(topic_id, user_id)
        with conn:
            if body.status:
                conn.execute("UPDATE topics SET status = ? WHERE id = ? AND user_id = ?", (body.status.value, topic_id, user_id))
            if body.revised:
                conn.execute("UPDATE topics SET revisions = revisions + 1 WHERE id = ? AND user_id = ?", (topic_id, user_id))
        return dict(own_topic(topic_id, user_id))

    @app.delete("/topics/{topic_id}", status_code=204)
    def delete_topic(topic_id: int, user_id: int = Depends(current_user)):
        own_topic(topic_id, user_id)
        with conn:
            conn.execute("DELETE FROM topics WHERE id = ? AND user_id = ?", (topic_id, user_id))

    @app.get("/stats")
    def stats(user_id: int = Depends(current_user)):
        rows = conn.execute("SELECT category, status, COUNT(*) AS n, SUM(revisions) AS rev FROM topics WHERE user_id = ? GROUP BY category, status", (user_id,))
        out = {}
        for r in rows:
            c = out.setdefault(r["category"], {"todo": 0, "doing": 0, "done": 0, "revisions": 0})
            c[r["status"]] = r["n"]; c["revisions"] += r["rev"] or 0
        return out

    return app


app = create_app()
