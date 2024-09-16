from src.adapters.sqlalchemy.db.session import SessionLocal


class SQLAlchemyRepo:
    def __init__(self, session: SessionLocal) -> None:
        self._session = session
