import streamlit as st
import db
import pandas as pd

st.header("📊 Raporlar")
st.caption("Çalışan ve firma bazında yapılacak ve tamamlanan işleri görüntüleyin.")

# Verileri al
tasks = db.list_tasks()
if not tasks:
    st.info("Henüz görev bulunmuyor.")
    st.stop()

# DataFrame'e dönüştür
df = pd.DataFrame(tasks, columns=["ID", "Firma", "Çalışan", "Görev", "Tarih", "Durum", "Notlar"])

tab1, tab2 = st.tabs(["👤 Çalışan Bazlı", "🏢 Firma Bazlı"])

# --------------------------------------------------
# TAB 1: ÇALIŞAN BAZLI RAPOR
# --------------------------------------------------
with tab1:
    employees = sorted(df["Çalışan"].dropna().unique())
    if not len(employees):
        st.warning("Hiç çalışan tanımlı değil.")
    else:
        selected_emp = st.selectbox("Çalışan Seç", employees)

        df_emp = df[df["Çalışan"] == selected_emp]
        pending = df_emp[df_emp["Durum"] == "Beklemede"]
        done = df_emp[df_emp["Durum"] == "Tamamlandı"]

        st.subheader(f"🕓 {selected_emp} - Yapılacak İşler")
        if pending.empty:
            st.write("Tüm işler tamamlanmış 🎉")
        else:
            st.dataframe(pending[["Firma", "Görev", "Tarih"]], use_container_width=True)

        st.subheader(f"✅ {selected_emp} - Tamamlanan İşler")
        if done.empty:
            st.write("Henüz tamamlanan iş yok.")
        else:
            st.dataframe(done[["Firma", "Görev", "Tarih"]], use_container_width=True)

# --------------------------------------------------
# TAB 2: FİRMA BAZLI RAPOR
# --------------------------------------------------
with tab2:
    firms = sorted(df["Firma"].dropna().unique())
    if not len(firms):
        st.warning("Hiç firma tanımlı değil.")
    else:
        selected_firm = st.selectbox("Firma Seç", firms)

        df_firm = df[df["Firma"] == selected_firm]
        pending = df_firm[df_firm["Durum"] == "Beklemede"]
        done = df_firm[df_firm["Durum"] == "Tamamlandı"]

        st.subheader(f"🕓 {selected_firm} - Yapılacak İşler")
        if pending.empty:
            st.write("Tüm işler tamamlanmış 🎉")
        else:
            st.dataframe(pending[["Çalışan", "Görev", "Tarih"]], use_container_width=True)

        st.subheader(f"✅ {selected_firm} - Tamamlanan İşler")
        if done.empty:
            st.write("Henüz tamamlanan iş yok.")
        else:
            st.dataframe(done[["Çalışan", "Görev", "Tarih"]], use_container_width=True)
import streamlit as st
import db
from datetime import datetime, timedelta

st.divider()
st.subheader("🧹 Otomatik Temizlik")

st.write(
    "Tamamlanmış görevler 30 günden sonra sistemden silinir. "
    "Bu işlemi manuel olarak da hemen başlatabilirsiniz."
)

if st.button("🧹 30 Günden Eski Tamamlanan Görevleri Temizle"):
    db.delete_old_completed_tasks()
    st.success("30 günden eski tamamlanmış görevler silindi ✅")
