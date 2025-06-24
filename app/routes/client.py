from flask import Blueprint, jsonify
from ..models import User
from ..extensions import db
from ..utils import verify_token

client_bp = Blueprint("client_bp", __name__)

@client_bp.route("/verify/<token>", methods=["GET"])
def verify_email(token):
    email = verify_token(token, salt="email-confirm")
    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.verified = True
    db.session.commit()
    return jsonify({"msg": "Email verified successfully!"})
