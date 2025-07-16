/app.py             # Beranda (opsional, bisa kosong atau info umum)
/pages/Regresi.py   # Halaman untuk input dan hitung regresi
/pages/Konsentrasi.py  # Halaman untuk hitung konsentrasi dari absorbansi
/pages/Akurasi.py      # Halaman evaluasi akurasi (%Recovery)

import streamlit as st

st.set_page_config(
    page_title="🧪 Aplikasi Analisis Regresi & Evaluasi",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🧪 Aplikasi Analisis Regresi dan Evaluasi Kinerja Metode")
st.markdown("""
Selamat datang di aplikasi analisis data spektrofotometri.

Gunakan sidebar untuk memilih menu:

- Regresi
- Hitung Konsentrasi
- Evaluasi Akurasi
""")
import streamlit as st
import numpy as np
import pandas as pd

def parse_numbers(text):
    try:
        return np.array([float(x.strip()) for x in text.split(",") if x.strip() != ""])
    except:
        return None

def linear_regression(x, y):
    n = len(x)
    sum_x, sum_y = np.sum(x), np.sum(y)
    sum_xx, sum_xy = np.sum(x**2), np.sum(x*y)
    denom = n * sum_xx - sum_x**2
    if denom == 0:
        return None, None, None
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    y_pred = slope * x + intercept
    ss_tot = np.sum((y - np.mean(y))**2)
    ss_res = np.sum((y - y_pred)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    return slope, intercept, r2

st.header("🔢 Input Data Standar dan Hitung Regresi")

conc_str = st.text_area("📏 Konsentrasi (ppm)", "0, 1, 2, 3, 4, 5")
abs_str = st.text_area("📊 Absorbansi", "0.005, 0.105, 0.205, 0.305, 0.405, 0.505")

if st.button("⚗ Hitung dan Tampilkan Regresi"):
    x = parse_numbers(conc_str)
    y = parse_numbers(abs_str)

    if x is None or y is None:
        st.error("Format data salah, hanya angka dipisah koma yang diperbolehkan.")
    elif len(x) < 2 or len(y) < 2:
        st.error("Minimal input 2 data.")
    elif len(x) != len(y):
        st.error(f"Jumlah data tidak sama: {len(x)} vs {len(y)}")
    else:
        slope, intercept, r2 = linear_regression(x, y)
        if None in [slope, intercept, r2]:
            st.error("Gagal menghitung regresi, periksa data Anda.")
        else:
            st.session_state.slope = slope
            st.session_state.intercept = intercept
            st.session_state.r2 = r2
            st.session_state.reg_ready = True

            st.success(f"Persamaan regresi: y = {slope:.4f} x + {intercept:.4f}")
            st.caption(f"Koefisien Determinasi (R²): {r2:.4f}")

            # Grafik
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.scatter(x, y, label="Data Standar", color="blue")
            x_line = np.linspace(min(x), max(x), 100)
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, color="red", label="Garis Regresi")
            ax.set_xlabel("Konsentrasi (ppm)")
            ax.set_ylabel("Absorbansi")
            ax.legend()
            st.pyplot(fig)
else:
    if st.session_state.get("reg_ready", False):
        st.info("Regresi sudah pernah dihitung. Pergi ke menu lain untuk gunakan nilai regresi.")
    else:
        st.info("Masukkan data dan tekan tombol di atas untuk menghitung regresi.")
import streamlit as st
import numpy as np
import pandas as pd

st.header("🧪 Hitung Konsentrasi dari Absorbansi Sampel")

if not st.session_state.get("reg_ready", False):
    st.warning("Harap lakukan regresi dahulu di menu Regresi.")
else:
    slope = st.session_state.slope
    intercept = st.session_state.intercept

    abs_str = st.text_area("Masukkan Absorbansi Sampel (dipisah koma)", "0.250, 0.255, 0.248")

    def parse_numbers(text):
        try:
            return np.array([float(x.strip()) for x in text.split(",") if x.strip() != ""])
        except:
            return None

    if st.button("Hitung Konsentrasi"):
        ys = parse_numbers(abs_str)
        if ys is None or len(ys) == 0:
            st.error("Format input absorbansi salah.")
        else:
            try:
                c_terukur = (ys - intercept) / slope
            except Exception as e:
                st.error(f"Error menghitung konsentrasi: {e}")
                c_terukur = np.array([])

            if len(c_terukur):
                df = pd.DataFrame({
                    "Absorbansi": ys,
                    "C-terukur (ppm)": c_terukur
                })
                st.dataframe(df.style.format({"Absorbansi": "{:.4f}", "C-terukur (ppm)": "{:.4f}"}), use_container_width=True)

                mean_val = np.mean(c_terukur)
                std_dev = np.std(c_terukur, ddof=0)
                st.success(f"Rata-rata konsentrasi: {mean_val:.4f} ppm, Std Deviasi: {std_dev:.4f}")

                # Hitung presisi (%RSD)
                rsd = (std_dev / mean_val) * 100 if mean_val != 0 else 0
                def classify_rsd(val):
                    if val <= 2:
                        return "🌟 Presisi Luar Biasa!"
                    elif val <= 5:
                        return "🟢 Presisi Sangat Baik!"
                    elif val <= 10:
                        return "🟡 Presisi Cukup Baik"
                    else:
                        return "🔴 Presisi Perlu Diperbaiki"
                st.info(f"Presisi (%RSD): {rsd:.2f}% — {classify_rsd(rsd)}")
import streamlit as st

st.header("✅ Evaluasi Akurasi (%Recovery)")

def to_float(x):
    try:
        return float(x)
    except:
        return None

c_spike_measured = st.text_input("🧪 C-spike terukur (ppm)", "0")
c_spike_added = st.text_input("➕ C-spike ditambahkan (ppm)", "0")
c_sample_initial = st.text_input("🔬 C-sampel awal (ppm)", "0")

if st.button("Hitung %Recovery"):
    measured = to_float(c_spike_measured)
    added = to_float(c_spike_added)
    initial = to_float(c_sample_initial)

    if None in [measured, added, initial]:
        st.error("Semua input harus angka valid.")
    elif added == 0:
        st.error("C-spike ditambahkan harus > 0.")
    else:
        recovery = ((measured - initial) / added) * 100

        if 95 <= recovery <= 105:
            status = "🌟 Akurasi Sempurna!"
        elif 90 <= recovery <= 110:
            status = "🟢 Akurasi Sangat Baik!"
        elif 80 <= recovery <= 120:
            status = "🟡 Akurasi Cukup Baik"
        else:
            status = "🔴 Akurasi Perlu Diperbaiki"

        st.success(f"%Recovery = {recovery:.2f}% — {status}")
        st.caption("Formula: ((C-spike terukur - C-sampel awal) / C-spike ditambahkan) × 100%")
