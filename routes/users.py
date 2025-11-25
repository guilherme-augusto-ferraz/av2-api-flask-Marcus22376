from flask import Blueprint, request, jsonify
from models.user import User
from database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint("users", __name__, url_prefix="/api/users")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "username, email e password são obrigatórios"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "username ou email já estão em uso"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuário registrado com sucesso", "user": user.to_dict()}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    identifier = data.get("identifier")  # pode ser username ou email
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"msg":"identifier e password são obrigatórios"}), 400

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    return jsonify({"user": user.to_dict()}), 200
