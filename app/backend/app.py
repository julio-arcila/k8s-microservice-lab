from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres-svc")
DB_NAME = os.environ.get("DB_NAME", "tasks")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASS = os.environ.get("DB_PASS", "secret123")

def get_db():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{"id": r[0], "title": r[1], "done": r[2]} for r in rows])

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id", (data["title"],))
    row = cur.fetchone()
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"id": row[0], "title": data["title"], "done": False}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
