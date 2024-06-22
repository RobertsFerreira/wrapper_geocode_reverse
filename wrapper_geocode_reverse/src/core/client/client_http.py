import requests


def get_client():
    with requests.Session() as session:
        yield session
