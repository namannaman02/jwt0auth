from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from typing import Dict, Set

app = Flask(__name__)

# Configuration for JWT
class Config:
    JWT_SECRET_KEY: str = 'your_secret_key'  # Replace with a strong secret key
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)

app.config.from_object(Config)
jwt = JWTManager(app)

# In-memory storage
users: Dict[str, str] = {}  # Email to hashed_password mapping
revoked_tokens: Set[str] = set()


@app.route('/signup', methods=['POST'])
def signup() -> tuple[dict, int]:
    """Register a new user with email and password."""
    data = request.get_json()
    email: str = data.get('email')
    password: str = data.get('password')

    if not email or not password:
        return {"msg": "Email and password are required"}, 400

    if email in users:
        return {"msg": "User already exists"}, 409

    users[email] = generate_password_hash(password)
    return {"msg": "User created successfully"}, 201


@app.route('/signin', methods=['POST'])
def signin() -> tuple[dict, int]:
    """Authenticate user and issue a token."""
    data = request.get_json()
    email: str = data.get('email')
    password: str = data.get('password')

    hashed_password = users.get(email)
    if not hashed_password or not check_password_hash(hashed_password, password):
        return {"msg": "Invalid credentials"}, 401

    token = create_access_token(identity=email)
    return {"access_token": token}, 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected() -> tuple[dict, int]:
    """Access a protected route."""
    current_user = get_jwt_identity()
    return {"msg": f"Hello, {current_user}!"}, 200


@app.route('/revoke', methods=['POST'])
@jwt_required()
def revoke() -> tuple[dict, int]:
    """Revoke the current user's token."""
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return {"msg": "Token revoked"}, 200


@app.route('/refresh', methods=['POST'])
@jwt_required()
def renew() -> tuple[dict, int]:
    """Renew the token if it hasn't been revoked."""
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return {"access_token": new_token}, 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header: dict, jwt_payload: dict) -> bool:
    """Check if a token has been revoked."""
    return jwt_payload["jti"] in revoked_tokens


@app.errorhandler(401)
def custom_401(error) -> tuple[dict, int]:
    """Handle unauthorized errors."""
    return {"msg": "Unauthorized", "error": str(error)}, 401


if __name__ == '__main__':
    app.run(debug=True)
