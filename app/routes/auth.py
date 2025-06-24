from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from ..extensions import db, bcrypt
from ..models import User
from ..utils import generate_token, send_email, verify_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 400

    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'], password_hash=hashed_pw, role='client')
    db.session.add(user)
    db.session.commit()


    subject = "Verify your email"
    recipient = user.email
    token = generate_token(user.email, salt='email-confirm')
    verify_url = f"{request.host_url}client/verify/{token}"
    body = f"Click the link to verify your account: {verify_url}"

    send_email(subject=subject, recipient=recipient, body=body)

    return jsonify({'msg': 'Signup successful. Check your email to verify.'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    if user.role == 'client' and not user.verified:
        return jsonify({'msg': 'Email not verified'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'access_token': access_token}), 200
