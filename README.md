# JWT Authentication in Flask

A simple Flask application implementing JWT authentication using **Flask-JWT-Extended**. The project provides basic endpoints for signup, signin, token-based protection, token revocation, and token refresh.

---

## Initial Setup

### 1. Create and Activate a Virtual Environment
```bash
python3 -m venv path/to/venv
source path/to/venv/bin/activate
```

### 2. Install Dependencies
```bash
python3 -m pip install flask flask-jwt-extended werkzeug
```

### 3. Run the Application
```bash
python3 app.py
```

---

## Endpoints

### 1. **Signup**
**Description**: Register a new user with email and password.  
**Endpoint**: `POST /signup`  
**Curl Command**:
```bash
curl --location 'http://127.0.0.1:5000/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "abc@abc.com",
    "password": "abc123"
}'
```

---

### 2. **Signin**
**Description**: Authenticate a user and issue an access token.  
**Endpoint**: `POST /signin`  
**Curl Command**:
```bash
curl --location 'http://127.0.0.1:5000/signin' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "abc@abc.com",
    "password": "abc123"
}'
```

---

### 3. **Protected Route**
**Description**: Access a route that requires authentication using an access token.  
**Endpoint**: `GET /protected`  
**Curl Command**:
```bash
curl --location 'http://127.0.0.1:5000/protected' \
--header 'Authorization: Bearer <your_access_token>'
```

---

### 4. **Revoke Token**
**Description**: Revoke the current access token to make it invalid for future requests.  
**Endpoint**: `POST /revoke`  
**Curl Command**:
```bash
curl --location 'http://127.0.0.1:5000/revoke' \
--header 'Authorization: Bearer <your_access_token>'
```

---

### 5. **Refresh Token**
**Description**: Renew an access token before it expires.  
**Endpoint**: `POST /refresh`  
**Curl Command**:
```bash
curl --location 'http://127.0.0.1:5000/refresh' \
--header 'Authorization: Bearer <your_access_token>'
```

---

## Key Features
1. **Token-Based Authentication**:
   - Uses JSON Web Tokens (JWT) for secure authentication.

2. **Token Revocation**:
   - Supports revoking tokens, preventing their further use.

3. **Secure Token Refresh**:
   - Allows renewing tokens while ensuring revoked tokens cannot be refreshed.

4. **Error Handling**:
   - Proper error codes and descriptive messages for failure scenarios.

---

## Example Workflow

1. **Sign Up**:
   Register a new user using the `/signup` endpoint.

2. **Sign In**:
   Authenticate using `/signin` to receive an access token.

3. **Access Protected Resources**:
   Use the `/protected` endpoint with the token to access secured resources.

4. **Revoke Token**:
   Revoke the token with `/revoke` to log out or invalidate a token.

5. **Refresh Token**:
   Renew the token using `/refresh` before it expires.

---

## Requirements
- **Python Version**: 3.13.0 or later  
- **Dependencies**:
  - Flask
  - Flask-JWT-Extended
  - Werkzeug

---

## Notes
- Replace `your_access_token` in the curl commands with the actual token received during signin.
- Update the `JWT_SECRET_KEY` in the code to a strong, unique key for production use.  
