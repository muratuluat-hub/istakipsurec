import streamlit as st
import db

st.header("🏢 Firma & 👤 Çalışan Tanımı")
st.write("Firmaları ve çalışanları bağımsız şekilde tanımlayabilirsiniz.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Firma Ekle")
    with st.form("firma_form", clear_on_submit=True):
        firm_name = st.text_input("Firma Adı")
        submitted = st.form_submit_button("Ekle")
        if submitted and firm_name:
            db.add_firm(firm_name)
            st.success(f"{firm_name} firması eklendi.")

with col2:
    st.subheader("Çalışan Ekle")
    with st.form("calisan_form", clear_on_submit=True):
        emp_name = st.text_input("Çalışan Adı")
        submitted = st.form_submit_button("Ekle")
        if submitted and emp_name:
            db.add_employee(emp_name)
            st.success(f"{emp_name} eklendi.")
st.divider()
st.subheader("⚙️ Kayıt Yönetimi")

# -------- FİRMA DÜZENLE / SİL --------
firms = db.list_firms()
if firms:
    st.write("**Firmalar:**")
    for f in firms:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_name = st.text_input(
                f"Firma adı düzenle ({f[1]})",
                value=f[1],
                key=f"firm_edit_{f[0]}_{f[1]}"
            )
        with col2:
            if st.button("🖊️ Güncelle", key=f"update_firm_{f[0]}_{f[1]}"):
                db.update_firm(f[1], new_name)
                st.success(f"{f[1]} → {new_name} olarak güncellendi.")
        with col3:
            if st.button("🗑️ Sil", key=f"delete_firm_{f[0]}_{f[1]}"):
                db.delete_firm(f[1])
                st.warning(f"{f[1]} silindi.")
else:
    st.info("Henüz firma eklenmemiş.")

st.divider()

# -------- ÇALIŞAN SİLME --------
employees = db.list_employees()
if employees:
    st.write("**Çalışanlar:**")
    for e in employees:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(e[1])
        with col2:
            if st.button("🗑️ Sil", key=f"delete_emp_{e[0]}_{e[1]}"):
                db.delete_employee(e[1])
                st.warning(f"{e[1]} silindi.")
else:
    st.info("Henüz çalışan eklenmemiş.")
