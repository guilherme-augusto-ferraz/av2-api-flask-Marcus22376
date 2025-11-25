from database import db
from datetime import datetime

class Registro(db.Model):
    __tablename__ = "registros"
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="registros")

    def to_dict(self):
        return {
            "id": self.id,
            "valor": self.valor,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "data": self.data.isoformat(),
            "tipo": self.tipo,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }
