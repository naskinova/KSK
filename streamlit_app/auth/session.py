import streamlit as st

def save_session(data: dict):
    st.session_state["user"] = {
        "id": data["user"]["id"],
        "email": data["user"]["email"],
        "name": data["user"]["name"],
        "role": data["user"]["role"],
        "must_change_password": data["user"]["must_change_password"],
        "access_token": data["access_token"]
    }

def is_logged_in():
    return "user" in st.session_state

def get_current_user():
    return st.session_state.get("user", {})
