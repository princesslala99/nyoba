import streamlit as st
import pandas as pd
import numpy as np
import math

# Fungsi menghitung CV Horwitz (untuk contoh, konsentrasi diasumsikan input pengguna)
def hitung_cv_horwitz(c):
    # c dalam fraksi (misal 0.01 untuk 1%)
    if c <= 0:
        return None
    return 2 * (10 ** (1 - 0.5 * math.log10(c)))

# Fungsi halaman cover
def cover_page():
    st.title("Selamat Datang di Aplikasi Kalkulator Kimia")
    st.markdown("""
    ### Aplikasi ini dapat menghitung:
    - %RSD (Relative Standard Deviation)
    - %RPD (Relative Percent Difference)
    - %Recovery
    
    Gunakan menu di sidebar untuk navigasi ke fitur yang diinginkan.
    """)
    st.image("https://images.unsplash.com/photo-1581093588401-9c0e7e0e8d5b?auto=format&fit=crop&w=800&q=60",
             caption="Ilustrasi Kimia", use_column_width=True)

# Fungsi halaman input data dalam bentuk tabel
def input_data_page():
    st.header("Input Data dalam Bentuk Tabel")

    if 'data_df' not in st.session_state:
        st.session_state['data_df'] = pd.DataFrame({'Data': [np.nan]*5})

    edited_df = st.data_editor(
        st.session_state['data_df'],
        num_rows="dynamic",
        use_container_width=True,
        key='data_editor'
    )

    st.session_state['data_df'] = edited_df

    data = edited_df['Data'].dropna().tolist()
    if len(data) > 0:
        st.success(f"Data berhasil dimasukkan: {data}")
    else:
        st.info("Masukkan data minimal satu nilai.")

# Fungsi halaman perhitungan %RSD dan %RPD
def calculation_rsd_rpd_page():
    st.header("Perhitungan %RSD & %RPD")

    if 'data_df' not in st.session_state:
        st.info("Silakan masukkan data terlebih dahulu pada menu 'Input Data'.")
        return

    data = st.session_state['data_df']['Data'].dropna().tolist()
    if len(data) == 0:
        st.info("Data kosong, silakan masukkan data pada menu 'Input Data'.")
        return

    arr = np.array(data)
    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    rsd = (std / mean) * 100 if mean != 0 else 0

    st.write(f"*Mean:* {mean:.3f}")
    st.write(f"*Std Dev:* {std:.3f}")
    st.write(f"%RSD:** {rsd:.2f}%")

    # Input konsentrasi untuk hitung CV Horwitz dan batas RSD
    st.markdown("---")
    st.subheader("Validasi Presisi berdasarkan CV Horwitz")
    konsentrasi_percent = st.number_input("Masukkan konsentrasi analit (%) untuk hitung CV Horwitz", min_value=0.0001, format="%.6f")
    konsentrasi_frac = konsentrasi_percent / 100

    if konsentrasi_frac > 0:
        cv_horwitz = hitung_cv_horwitz(konsentrasi_frac)
        batas_rsd = 0.5 * cv_horwitz  # Syarat keberterimaan RSD ≤ ½ CV Horwitz
        st.write(f"Nilai CV Horwitz: {cv_horwitz:.2f}%")
        st.write(f"Batas keberterimaan %RSD: ≤ {batas_rsd:.2f}%")

        if rsd <= batas_rsd:
            st.success("Nilai %RSD memenuhi syarat keberterimaan presisi.")
        else:
            st.error("Nilai %RSD TIDAK memenuhi syarat keberterimaan presisi.")
    else:
        st.info("Masukkan konsentrasi analit untuk validasi presisi.")

    # Hitung %RPD jika data dua titik
    if len(arr) == 2:
        rpd = (abs(arr[0] - arr[1]) / ((arr[0] + arr[1]) / 2)) * 100
        st.write(f"%RPD:** {rpd:.2f}%")

        # Syarat keberterimaan %RPD umum: ≤ 10% (bisa disesuaikan)
        batas_rpd = 10.0
        if rpd <= batas_rpd:
            st.success(f"Nilai %RPD ({rpd:.2f}%) memenuhi syarat keberterimaan (≤ {batas_rpd}%).")
        else:
            st.error(f"Nilai %RPD ({rpd:.2f}%) TIDAK memenuhi syarat keberterimaan (≤ {batas_rpd}%).")
    else:
        st.info("Masukkan tepat dua data untuk menghitung %RPD.")

# Fungsi halaman perhitungan %Recovery
def calculation_recovery_page():
    st.header("Perhitungan %Recovery")

    hasil = st.number_input("Hasil pengujian (hasil ditemukan)", value=0.0)
    spike = st.number_input("Nilai spike (nilai yang ditambahkan)", value=0.0)

    if spike != 0:
        recovery = (hasil / spike) * 100
        st.write(f"%Recovery:** {recovery:.2f}%")

        # Syarat keberterimaan recovery umumnya 85% - 115%
        if 85 <= recovery <= 115:
            st.success("Nilai %Recovery memenuhi syarat keberterimaan (85% - 115%).")
        else:
            st.error("Nilai %Recovery TIDAK memenuhi syarat keberterimaan (85% - 115%).")
    else:
        st.info("Masukkan nilai spike lebih dari 0.")

# --- Main aplikasi ---

st.set_page_config(page_title="Kalkulator Kimia", page_icon="⚗", layout="centered")

# Sidebar menu
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", 
                        ["Cover", "Input Data", "Perhitungan %RSD & %RPD", "Perhitungan %Recovery"])

# Routing halaman berdasarkan pilihan menu
if menu == "Cover":
    cover_page()
elif menu == "Input Data":
    input_data_page()
elif menu == "Perhitungan %RSD & %RPD":
    calculation_rsd_rpd_page()
elif menu == "Perhitungan %Recovery":
    calculation_recovery_page()
