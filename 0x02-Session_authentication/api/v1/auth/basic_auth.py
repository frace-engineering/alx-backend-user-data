#!/usr/bin/env python3
"""Authentication class"""
from flask import request
from .auth import Auth
from typing import List, TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic class authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Process the base64 part of the authorization header"""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode the base64 header"""
        base64_string = base64_authorization_header
        if base64_string is None or not isinstance(base64_string, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except ValueError:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract the user email and password from base64 encoding"""
        base64_string = decoded_base64_authorization_header
        if base64_string is None or not isinstance(base64_string, str):
            return None, None
        if ':' not in base64_string:
            return None, None
        user_email, user_password = base64_string.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Return user instance bsed on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({'email': user_email})
        if not user_list:
            return None
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrive user instance for a request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decode_string = self.decode_base64_authorization_header(b64_header)
        user_email, user_pwd = self.extract_user_credentials(decode_string)
        user_instance = self.user_object_from_credentials(user_email, user_pwd)

        return user_instance
