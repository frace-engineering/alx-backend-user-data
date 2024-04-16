#!/usr/bin/env python3
"""Authentication class"""
from flask import request
from .auth import Auth


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
            return authorization_header.split(' ')[1:]
