# streamlit_app/examiner/api.py
import streamlit as st
import requests
from app.config import settings

BACKEND_URL = settings.BACKEND_URL


def save_grades(payload: list[dict]) -> bool:
    """Send grades to backend."""
    try:
        token = st.session_state.user["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{BACKEND_URL}/grades/save", json=payload, headers=headers)
        st.write("📤 POST /grades/save", response.status_code, response.text)
        return response.status_code == 200
    except Exception as e:
        st.error(f"⚠️ Неуспешно изпращане на оценки: {e}")
        return False


def fetch_assigned_students() -> list[int]:
    """Get student IDs assigned to the examiner."""
    try:
        token = st.session_state.user["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/grades/assigned/me", headers=headers)
        if response.status_code == 200:
            return response.json().get("student_ids", [])
        else:
            st.warning(f"⚠️ Грешка при зареждане на студентски ID: {response.text}")
            return []
    except Exception as e:
        st.warning(f"⚠️ Неуспешно зареждане на студентски ID: {e}")
        return []


def fetch_existing_grades() -> list[dict]:
    """Fetch existing grades submitted by the examiner."""
    try:
        token = st.session_state.user["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/grades/my-submissions", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"⚠️ Грешка при зареждане на оценки: {response.text}")
            return []
    except Exception as e:
        st.error(f"⚠️ Неуспешно извличане на оценки: {e}")
        return []
