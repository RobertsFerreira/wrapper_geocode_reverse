from pytest import Session
from sqlalchemy import create_engine

from wrapper_geocode_reverse.src.core.settings.settings import Settings

settings = Settings()  # type: ignore


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:  # type: ignore
        yield session
