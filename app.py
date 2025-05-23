from flask import Flask, request, jsonify
from services.auth_service import AuthService
from services.task_service import TaskService
from utils.jwt_manager import generate_token, jwt_required

app = Flask(__name__)
auth_service = AuthService()
task_service = TaskService()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"message": "Username y password son requeridos"}), 400
    if len(password) < 6:
        return jsonify({"message": "La contraseña debe tener al menos 6 caracteres"}), 400

    success, message = auth_service.register_user(username, password)
    return jsonify({"message": message}), 201 if success else 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"message": "Credenciales requeridas"}), 400

    if auth_service.authenticate_user(username, password):
        token = generate_token(username)
        return jsonify({"token": token})
    return jsonify({"message": "Credenciales incorrectas"}), 401

@app.route("/api/tasks", methods=["GET"])
@jwt_required
def get_tasks(username):
    tasks = task_service.get_tasks(username)
    return jsonify([{"title": t.title, "description": t.description} for t in tasks]), 200

@app.route("/api/tasks", methods=["POST"])
@jwt_required
def create_task(username):
    data = request.get_json()
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title:
        return jsonify({"message": "El título es obligatorio"}), 400

    task_service.add_task(username, title, description)
    return jsonify({"message": "Tarea creada"}), 201

if __name__ == "__main__":
    # HTTPS con certificados autofirmados
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
