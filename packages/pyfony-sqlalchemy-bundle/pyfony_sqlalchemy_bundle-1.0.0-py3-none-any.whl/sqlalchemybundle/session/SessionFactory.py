from sqlalchemy.orm.session import sessionmaker
from sqlalchemybundle.engine.EngineLazy import EngineLazy
from sqlalchemybundle.session.SessionLazy import SessionLazy


class SessionFactory:
    def create(self, engine_lazy: EngineLazy):
        def create_lazy():
            return sessionmaker(bind=engine_lazy.get)()

        return SessionLazy(create_lazy)
