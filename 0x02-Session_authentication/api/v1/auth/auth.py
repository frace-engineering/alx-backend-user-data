#!/usr/bin/env python3
"""Authentication class"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Evaluate the paths available to access only the required path"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excl_path in excluded_paths:
            if excl_path.endswith('*') and path.startswith(excl_path[:-1]):
                return False
        for p in excluded_paths:
            if path.rstrip('/') == p.rstrip('/'):
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Return Authorization if contained in request.header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None"""
        return None

    def session_cookie(self, request=None):
        """Return a cookie value"""
        if request is None:
            return None
        else:
            cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
            if cookie_name in request.cookies:
                return request.cookies.get(cookie_name)
            else:
                return None
