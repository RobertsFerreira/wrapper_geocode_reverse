from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from wrapper_geocode_reverse.src.core.settings.settings import get_settings

settings = get_settings()  # type: ignore


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:  # type: ignore
        yield session
