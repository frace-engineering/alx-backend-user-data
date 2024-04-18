#!/usr/bin/env python3
"""Creat session class"""
import uuid
from .auth import Auth


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Genarage session id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            self.session_id = str(uuid.uuid4())
            if self.session_id not in self.user_id_by_session_id:
                self.user_id_by_session_id[user_id] = {} 
            self.user_id_by_session_id[user_id] = self.session_id 
            return self.session_id
