from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings


class Base(DeclarativeBase):
    pass


def make_engine(url: str | None = None):
    value = url or get_settings().database_url
    return create_engine(
        value, connect_args={"check_same_thread": False} if value.startswith("sqlite") else {}
    )


engine = make_engine()
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def get_session():
    with SessionLocal() as session:
        yield session
