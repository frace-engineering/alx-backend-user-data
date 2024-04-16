#!/usr/bin/env python3
"""Authentication class"""
from flask import request
from .auth import Auth
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

        """
        if not base64_authorization_header.startswith('Basic '):
            return None
        else:
            return base64_authorization_header.split(' ')[1]
            """
