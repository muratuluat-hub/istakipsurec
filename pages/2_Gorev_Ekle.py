import streamlit as st
from datetime import date
import db

st.header("🗂️ Görev Ekle")

firms = db.list_firms()
employees = db.list_employees()

if not firms or not employees:
    st.warning("Görev eklemek için en az bir firma ve bir çalışan tanımlanmış olmalı.")
    st.stop()

selected_firm = st.selectbox("Firma Seç", [f[1] for f in firms])
selected_emp = st.selectbox("Çalışan Seç", [e[1] for e in employees])

firm_id = [f[0] for f in firms if f[1] == selected_firm][0]
employee_id = [e[0] for e in employees if e[1] == selected_emp][0]

task_name = st.text_input("Görev Tanımı")
due_date = st.date_input("Tamamlanma Tarihi", value=date.today())

if st.button("Görevi Kaydet"):
    db.add_task(firm_id, employee_id, task_name, str(due_date))
    st.success(f"{selected_emp} için '{task_name}' görevi eklendi.")
