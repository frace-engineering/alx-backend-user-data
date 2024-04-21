#!/usr/bin/env python3
"""Creat session class"""
import uuid
from flask import request
from .auth import Auth


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Genarage session id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        else:
            session_id = str(uuid.uuid4())
            """if self.session_id not in self.user_id_by_session_id:
                self.user_id_by_session_id[user_id] = {}"""
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the user_id of the session user"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None):
        """Delete the user session"""
        if self.request is None:
            return None
        session_id =  self.session_cookie(request)
        if not session_id:
            return False
        user_id =  self.user_id_by_session_id(session_id)
        if not user_id:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True
        else:
            return False

