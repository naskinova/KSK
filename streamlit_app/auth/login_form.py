# streamlit_app/auth/login_form.py
import pandas as pd
import streamlit as st
import sys
from pathlib import Path

# Add the root project directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from auth.api import login_user
from examiner.api import fetch_assigned_students, fetch_existing_grades


def render_login_form():
    st.subheader("🔐 Вход за проверяващи и администратори")

    email = st.text_input("Имейл")
    password = st.text_input("Парола", type="password")

    if st.button("Вход"):
        # 🧠 Извикване на бекенда
        response = login_user(email, password)

        if response:
            # ✅ Записване на потребителските данни
            user = response["user"]
            access_token = response["access_token"]
            st.session_state.user = user
            st.session_state.user["access_token"] = access_token

            # ✅ Debug print
            st.info("👤 Данни за потребителя:")
            st.json(user)  # Покажи целия обект

            st.success(f"Добре дошъл, {user['name']}! ({user['role']})")
            st.write("🔐 Токен:")
            st.code(user["access_token"], language="bash")

            # 🎓 Само за проверяващи
            if user["role"] == "examiner":
                st.info("🔄 Зареждане на студентите и въведените оценки...")

                assigned = fetch_assigned_students()
                st.session_state.assigned_students = assigned or []

                grades = fetch_existing_grades()
                if grades and isinstance(grades, list) and len(grades) > 0:
                    df = pd.DataFrame(grades)
                    st.session_state.grades_df = df
                    st.success(f"✅ Заредени оценки за {len(df)} студента.")
                else:
                    st.session_state.grades_df = pd.DataFrame()
                    st.info("ℹ️ Няма въведени оценки до момента.")
            else:
                # За други роли
                st.session_state.assigned_students = []
                st.session_state.grades_df = pd.DataFrame()

            st.success("✅ Успешен вход!")
            st.rerun()
        else:
            st.error("❌ Невалиден имейл или парола.")
