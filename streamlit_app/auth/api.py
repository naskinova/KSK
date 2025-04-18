import requests
from dynaconf import settings


def login_user(email: str, password: str):
    try:
        response = requests.post(f"{settings.BACKEND_URL}/auth/login", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Login error:", e)
        return None
