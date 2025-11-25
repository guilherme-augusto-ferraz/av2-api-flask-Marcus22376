from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db
from routes.users import bp as users_bp
from routes.registros import bp as registros_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    init_db(app)
    jwt = JWTManager(app)

    # blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(registros_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"msg":"Endpoint não encontrado"}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
