from pydantic_settings import BaseSettings, SettingsConfigDict

from wrapper_geocode_reverse.src.core.logger.logger import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    DATABASE_URL: str
    SPATIALITE_DLL_URL: str
    OPEN_ROUTER_TOKEN: str
    OPEN_ROUTER_GEOCODE_REVERSE_URL: str

    def __repr__(self) -> str:
        return f"""
                    Settings(
                        DATABASE_URL={self.DATABASE_URL},
                        SpatIALITE_DLL_URL={self.SPATIALITE_DLL_URL},
                        OPEN_ROUTER_GEOCODE_REVERSE_URL={self.OPEN_ROUTER_GEOCODE_REVERSE_URL}
                        )
                    """


def get_settings():
    settings = Settings()  # type: ignore
    logger.debug('Loading settings')
    return settings
