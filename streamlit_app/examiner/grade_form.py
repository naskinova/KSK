# streamlit_app/examiner/grade_form.py
import streamlit as st
import pandas as pd
from io import BytesIO
import sys
from pathlib import Path

# Add root path to allow absolute imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from examiner.api import save_grades, fetch_assigned_students, fetch_existing_grades

COLUMNS = ["student_id"] + [str(i) for i in range(1, 9)] + ["Общо"]
DEFAULT_ROWS = 10

def render_examiner_form():
    st.subheader("📋 Въвеждане на оценки")

    user = st.session_state.get("user")
    if not user or user.get("role") != "examiner":
        st.error("❌ Нямате достъп до тази страница.")
        st.stop()

    st.info(f"🧑‍🏫 Проверяващ: {user['name']} ({user['email']}, ID: {user['id']})")

    # Fetch student IDs if not cached
    if "assigned_students" not in st.session_state:
        st.session_state.assigned_students = fetch_assigned_students()

    assigned_ids = st.session_state.assigned_students

    # Fetch grades if not cached
    if "grades_df" not in st.session_state:
        existing = fetch_existing_grades()
        if existing:
            df = pd.DataFrame(existing)
            df["❌ Изтрий"] = False
        else:
            data = []
            for student_id in assigned_ids:
                row = {col: 0.0 for col in COLUMNS}
                row["student_id"] = student_id
                row["❌ Изтрий"] = False
                data.append(row)

            if not data:
                data = [{**{col: 0.0 for col in COLUMNS}, "student_id": "", "❌ Изтрий": False}
                        for _ in range(DEFAULT_ROWS)]
            df = pd.DataFrame(data)

        st.session_state.grades_df = df

    df = st.session_state.grades_df

    # 🧮 Recalculate totals
    for idx, row in df.iterrows():
        total = sum([float(row.get(str(i), 0)) for i in range(1, 9) if pd.notnull(row.get(str(i)))])
        df.at[idx, "Общо"] = round(total, 2)

    if "❌ Изтрий" not in df.columns:
        df["❌ Изтрий"] = False

    # ✏️ Editable Table
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_order=COLUMNS + ["❌ Изтрий"],
        key="grades_editor",
        hide_index=True,
    )
    st.session_state.grades_df = edited_df

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Добави ред"):
            new_row = {col: 0.0 for col in COLUMNS}
            new_row["student_id"] = ""
            new_row["❌ Изтрий"] = False
            st.session_state.grades_df = pd.concat(
                [st.session_state.grades_df, pd.DataFrame([new_row])],
                ignore_index=True
            )

    with col2:
        if st.button("🗑 Изтрий избраните редове"):
            df = st.session_state.grades_df
            if "❌ Изтрий" in df.columns:
                df_cleaned = df[df["❌ Изтрий"] != True].drop(columns=["❌ Изтрий"], errors="ignore")
                st.session_state.grades_df = df_cleaned.reset_index(drop=True)
                st.success("✅ Избраните редове са премахнати.")
            else:
                st.warning("❗ Няма избрани редове за изтриване.")

    st.markdown("---")

    # 📄 Preview
    if st.button("📄 Преглед на подадените оценки"):
        df_clean = st.session_state.grades_df.copy()
        df_clean = df_clean[df_clean["student_id"].astype(str).str.strip() != ""]
        df_preview = df_clean.drop(columns=["❌ Изтрий"], errors="ignore")
        st.dataframe(df_preview, use_container_width=True)

        output = BytesIO()
        df_preview.to_excel(output, index=False)
        st.download_button(
            label="⬇️ Изтегли като Excel",
            data=output.getvalue(),
            file_name="grades_preview.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # 💾 Save
    if st.button("💾 Запази резултатите"):
        df_clean = st.session_state.grades_df.copy()
        df_clean = df_clean[df_clean["student_id"].astype(str).str.strip() != ""]
        df_clean = df_clean.drop(columns=["❌ Изтрий"], errors="ignore")

        payload = df_clean[COLUMNS[:-1]].to_dict(orient="records")
        st.write("📦 Изпращане на:", payload)

        success = save_grades(payload)
        if success:
            st.success("✅ Всички оценки са записани успешно!")
        else:
            st.error("❌ Възникна грешка при записване на оценките.")
