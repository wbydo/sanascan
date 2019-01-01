from contextlib import ContextDecorator

from sqlalchemy.orm.session import Session as OriginalSession
from sqlalchemy.orm import sessionmaker

class _SNKSession(OriginalSession, ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        self.close()
        return False

    def commit_manager(self):
        return _CommitManager(self)

SNKSession = sessionmaker(class_=_SNKSession)

class _CommitManager:
    def __init__(self, snksession):
        self._s = snksession

    def __enter__(self):
        return self._s

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._s.rollback()
        else:
            self._s.commit()

        return False
