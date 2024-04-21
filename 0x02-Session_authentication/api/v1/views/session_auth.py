#!/usr/bin/env python3
"""Model for session_auth views"""
import os
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login
    Retieve email and password
    """
    if request.method == 'POST':
        email = request.form.get('email')
        if not email or email == '':
            return jsonify({"error": "email missing"}), 400
        password = request.form.get('password')
        if not password or password == '':
            return jsonify({"error": "password is missing"}), 400
        user_list = User.search({'email': email})
        if not user_list:
            return jsonify({"error": "no user found for this email"}), 404
        for user in user_list:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response_data = user.to_json()
                response = make_response(jsonify(response_data), 200)
                response.set_cookie(os.getenv('SESSION_NAME'), session_id)
                return response
            else:
                return jsonify({"error": "wrong password"}), 4004
        return jsonify({"error": "no user found for this email"}), 404

    @app_views.route('/api/v1/auth_session/logout', methods=['DELETE'],
                     strict_slashes=False)
    def logout():
        """DELETE /api/v1/auth_session/logout"""
        from api.v1.app import auth
        if self.auth.destroy_session(request):
            return jsonify({}), 200
        else:
            abort(404)
