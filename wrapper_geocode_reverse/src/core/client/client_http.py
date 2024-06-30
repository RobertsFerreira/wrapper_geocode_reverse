from httpx import Client


def get_client():
    with Client() as session:
        yield session
