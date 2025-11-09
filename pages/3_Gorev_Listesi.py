import streamlit as st
import db

st.header("📋 Görev Listesi")

tasks = db.list_tasks()
if not tasks:
    st.info("Henüz görev bulunmuyor.")
    st.stop()

for t in tasks:
    with st.expander(f"{t[1] or 'Firma Yok'} - {t[2] or 'Çalışan Yok'} | {t[3]}"):
        st.write(f"Tamamlanma Tarihi: {t[4]}")
        new_status = st.radio("Durum", ["Beklemede", "Tamamlandı"], index=0 if t[5]=='Beklemede' else 1, key=t[0])
        new_notes = st.text_area("Notlar", value=t[6] or "", key=f"note_{t[0]}")
        if st.button("Güncelle", key=f"btn_{t[0]}"):
            db.update_task(t[0], new_status, new_notes)
            st.success("Görev güncellendi!")
