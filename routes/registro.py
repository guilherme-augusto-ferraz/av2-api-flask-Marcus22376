from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.registro import Registro
from models.user import User
from datetime import datetime

bp = Blueprint("registros", __name__, url_prefix="/api/registros")

def parse_date(date_str):
    # espera YYYY-MM-DD
    return datetime.strptime(date_str, "%Y-%m-%d").date()

@bp.route("", methods=["POST"])
@jwt_required()
def create_registro():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    try:
        valor = float(data.get("valor"))
        categoria = data.get("categoria")
        descricao = data.get("descricao")
        data_field = parse_date(data.get("data"))
        tipo = data.get("tipo")
    except Exception as e:
        return jsonify({"msg":"Dados inválidos", "error": str(e)}), 400

    if tipo not in ("receita", "despesa"):
        return jsonify({"msg":"tipo deve ser 'receita' ou 'despesa'"}), 400

    registro = Registro(
        valor=valor,
        categoria=categoria,
        descricao=descricao,
        data=data_field,
        tipo=tipo,
        user_id=user_id
    )
    db.session.add(registro)
    db.session.commit()
    return jsonify({"msg":"Registro criado", "registro": registro.to_dict()}), 201

@bp.route("", methods=["GET"])
@jwt_required()
def list_registros():
    user_id = get_jwt_identity()
    registros = Registro.query.filter_by(user_id=user_id).all()
    return jsonify([r.to_dict() for r in registros]), 200

@bp.route("/<int:registro_id>", methods=["GET"])
@jwt_required()
def get_registro(registro_id):
    user_id = get_jwt_identity()
    registro = Registro.query.filter_by(id=registro_id, user_id=user_id).first()
    if not registro:
        return jsonify({"msg":"Registro não encontrado"}), 404
    return jsonify(registro.to_dict()), 200

@bp.route("/<int:registro_id>", methods=["PUT"])
@jwt_required()
def update_registro(registro_id):
    user_id = get_jwt_identity()
    registro = Registro.query.filter_by(id=registro_id, user_id=user_id).first()
    if not registro:
        return jsonify({"msg":"Registro não encontrado"}), 404

    data = request.get_json() or {}
    if "valor" in data:
        registro.valor = float(data.get("valor"))
    if "categoria" in data:
        registro.categoria = data.get("categoria")
    if "descricao" in data:
        registro.descricao = data.get("descricao")
    if "data" in data:
        registro.data = parse_date(data.get("data"))
    if "tipo" in data:
        tipo = data.get("tipo")
        if tipo not in ("receita","despesa"):
            return jsonify({"msg":"tipo deve ser 'receita' ou 'despesa'"}), 400
        registro.tipo = tipo

    db.session.commit()
    return jsonify({"msg":"Registro atualizado", "registro": registro.to_dict()}), 200

@bp.route("/<int:registro_id>", methods=["DELETE"])
@jwt_required()
def delete_registro(registro_id):
    user_id = get_jwt_identity()
    registro = Registro.query.filter_by(id=registro_id, user_id=user_id).first()
    if not registro:
        return jsonify({"msg":"Registro não encontrado"}), 404

    db.session.delete(registro)
    db.session.commit()
    return jsonify({"msg":"Registro excluído"}), 200
