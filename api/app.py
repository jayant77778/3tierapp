import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppass")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", future=True)

app = Flask(__name__)

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """))

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "up"})
    except Exception as e:
        return jsonify({"status": "down", "error": str(e)}), 500

@app.get("/users")
def list_users():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name FROM users ORDER BY id DESC")).mappings().all()
        return jsonify([{"id": r["id"], "name": r["name"]} for r in rows])

@app.post("/users")
def create_user():
    name = request.json.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users(name) VALUES (:n)"), {"n": name})
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
