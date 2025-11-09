import streamlit as st
import db

st.set_page_config(page_title="Görev Takip Sistemi", page_icon="📋", layout="centered")
db.init_db()

st.title("📋 Görev Takip Sistemi v2")
st.markdown("Firmalar ve çalışanlar artık birbirinden **bağımsız** tanımlanabilir.")

st.info("Menüden işlem seçin: Firma & Çalışan Tanımı, Görev Ekle veya Görev Listesi.")
