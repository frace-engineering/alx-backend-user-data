#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create aUser instance using email and hashed password.

        Args:
            email.
            hashed_password.

        Return:
            User instance.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Search the db to retrieve the first row found.

        Args:
            Any keyword argument.

        Return:
            First row found.
        """
        from sqlalchemy.orm.exc import NoResultFound
        from sqlalchemy.exc import InvalidRequestError
        try:
            session = self._session
            result = session.query(User).filter_by(**kwargs).first()
            if result is None:
                raise NoResultFound("Not found")
            return result
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid") from e

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """Update user attribute"""
        this_user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            if hasattr(this_user, attr):
                setattr(this_user, attr, value)
        self._session.commit()
