from flask import Flask, request, jsonify, send_from_directory
import os
from db import get_db, close_db

# フロントエンドのビルド済みファイルのパスを指定
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '../frontend/dist')

app = Flask(__name__, static_folder=FRONTEND_PATH, static_url_path='')
app.teardown_appcontext(close_db)

# ルートパスでindex.htmlを返す
@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/api/todos")
def list_todos():
    with get_db().cursor() as cur:
        cur.execute("SELECT id, title, done, created_at FROM todos ORDER BY id DESC")
        return jsonify(cur.fetchall())

@app.post("/api/todos")
def add_todo():
    title = (request.get_json() or {}).get("title","").strip()
    if not title: return {"error":"title required"}, 400
    with get_db().cursor() as cur:
        cur.execute("INSERT INTO todos(title, done) VALUES(%s, 0)", (title,))
    return {"ok": True}, 201

@app.post("/api/todos/<int:todo_id>/toggle")
def toggle(todo_id):
    with get_db().cursor() as cur:
        cur.execute("UPDATE todos SET done = 1 - done WHERE id=%s", (todo_id,))
    return {"ok": True}, 200
