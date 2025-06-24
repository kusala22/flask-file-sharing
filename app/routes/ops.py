from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import send_email

ops_bp = Blueprint("ops_bp", __name__)

@ops_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()

    if current_user['role'] != 'ops':
        return jsonify({"msg": "Access forbidden: ops users only"}), 403

    data = request.get_json()

    # Safely extract and cast to strings
    subject = str(data.get("subject", "")).strip()
    recipient = str(data.get("recipient", "")).strip()
    body = str(data.get("body", "")).strip()

    # Check for missing fields
    if not subject or not recipient or not body:
        return jsonify({"msg": "Missing required fields"}), 400

    # Debug: check types and values
    print("DEBUG SENDING EMAIL:")
    print("Subject Type:", type(subject), "| Value:", subject)
    print("Recipient Type:", type(recipient), "| Value:", recipient)
    print("Body Type:", type(body), "| Value:", body)

    try:
        send_email(subject=subject, recipient=recipient, body=body)
        return jsonify({"msg": "Email sent successfully."}), 200
    except Exception as e:
        return jsonify({"msg": f"Failed to send email: {str(e)}"}), 500
