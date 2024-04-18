#!/usr/bin/env python3
"""Creat session class"""
import uuid
from .auth import Auth


class SessionAuth(Auth):
    """Genarate the session id."""
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            if user_id not in self.user_id_by_session_id:
                self.user_id_by_session_id[user_id] = session_id 
            return session_id
