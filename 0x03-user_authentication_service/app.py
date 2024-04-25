#!/usr/bin/env python3
"""app.py
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """GET /"""
    return jsonify({"message": "Bienvenue"}), 200

@app.route('/users', methods=['POST'], strict_slashes=False)
def user():
    """POST /users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if AUTH.register_user(email, password):
            return jsonify({"email": f"{email}", "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
