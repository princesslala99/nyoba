import streamlit as st
import pandas as pd
import numpy as np
pip install matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Aplikasi Analisis Spektrofotometri", layout="centered")

def cover():
    st.title("Aplikasi Analisis Spektrofotometri")
    st.markdown("""
    Aplikasi ini membantu menghitung:
    - Kurva kalibrasi dari data deret standar absorbansi dan konsentrasi
    - Konsentrasi sampel berdasarkan kurva kalibrasi
    - Presisi (%RSD, %RPD) dari pengukuran konsentrasi
    - Akurasi (%Recovery) berdasarkan data spiking
    
    Ikuti menu di sidebar untuk proses bertahap.
    """)

def input_standards():
    st.header("1. Input Data Standar")
    st.markdown("Masukkan data konsentrasi (ppm) dan absorbansi deret standar.")

    if 'standar_df' not in st.session_state:
        df = pd.DataFrame({
            'Konsentrasi (ppm)': [0, 1, 2, 3, 4],
            'Absorbansi': [0.0, 0.1, 0.2, 0.3, 0.4]
        })
        st.session_state['standar_df'] = df
    else:
        df = st.session_state['standar_df']

    data = st.data_editor(df, num_rows="dynamic", key='standar_editor', use_container_width=True)
    st.session_state['standar_df'] = data

def plot_kalibrasi(data):
    # Buang row dengan data kosong
    data = data.dropna()

    X = data['Konsentrasi (ppm)'].values.reshape(-1,1)
    y = data['Absorbansi'].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = model.score(X, y)

    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Data Standar')
    ax.plot(X, y_pred, color='red', label='Kalibrasi Linear')
    ax.set_xlabel('Konsentrasi (ppm)')
    ax.set_ylabel('Absorbansi')
    ax.set_title(f'Kurva Kalibrasi (R² = {r2:.4f})')
    ax.legend()
    st.pyplot(fig)

    intercept = model.intercept_
    slope = model.coef_[0]
    return intercept, slope, r2

def hitung_konsentrasi(abs_sample, intercept, slope):
    if slope == 0:
        return 0
    return (abs_sample - intercept) / slope

def input_sample():
    st.header("2. Input Data Sampel")
    abs_sample = st.number_input("Masukkan absorbansi sampel", min_value=0.0, step=0.001, format="%.4f")
    return abs_sample

def input_precision_data():
    st.header("3. Input Data Presisi (Konsentrasi dari pengukuran berulang)")
    st.markdown("Masukkan data pengukuran konsentrasi sampel berulang untuk menghitung %RSD dan %RPD")
    if 'precision_df' not in st.session_state:
        df = pd.DataFrame({'Konsentrasi (ppm)': [np.nan, np.nan]})
        st.session_state['precision_df'] = df
    else:
        df = st.session_state['precision_df']
    data = st.data_editor(df, num_rows="dynamic", key="precision_editor", use_container_width=True)
    st.session_state['precision_df'] = data
    return data['Konsentrasi (ppm)'].dropna().tolist()

def input_recovery_data():
    st.header("4. Input Data Akurasi (%Recovery)")
    hasil = st.number_input("Hasil pengujian dengan spike", min_value=0.0, step=0.001, format="%.4f")
    hasil_asli = st.number_input("Hasil pengujian tanpa spike", min_value=0.0, step=0.001, format="%.4f")
    spike = st.number_input("Konsentrasi spike yang ditambahkan", min_value=0.0, step=0.001, format="%.4f")
    return hasil, hasil_asli, spike

def hitung_rsd(data):
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    rsd = (std / mean) * 100 if mean != 0 else 0
    return mean, std, rsd

def hitung_rpd(data):
    if len(data) != 2:
        return None
    rpd = abs(data[0] - data[1]) / ((data[0] + data[1]) / 2) * 100
    return rpd

def hitung_recovery(hasil_spike, hasil_asli, spike):
    if spike == 0:
        return None
    recovery = ((hasil_spike - hasil_asli) / spike) * 100
    return recovery

def tampilkan_kesimpulan_rsd(rsd):
    st.subheader("Kesimpulan Presisi (%RSD)")
    batas_rsd = 5  # contoh batas RSD maksimal 5%
    if rsd <= batas_rsd:
        st.success(f"%RSD = {rsd:.2f}% → Memenuhi syarat (≤ {batas_rsd}%)")
    else:
        st.error(f"%RSD = {rsd:.2f}% → Tidak memenuhi syarat (≤ {batas_rsd}%)")

def tampilkan_kesimpulan_rpd(rpd):
    st.subheader("Kesimpulan Presisi (%RPD)")
    if rpd is None:
        st.info("Masukkan tepat 2 data pengukuran untuk hitung %RPD")
        return
    batas_rpd = 10  # contoh batas RPD maksimal 10%
    if rpd <= batas_rpd:
        st.success(f"%RPD = {rpd:.2f}% → Memenuhi syarat (≤ {batas_rpd}%)")
    else:
        st.error(f"%RPD = {rpd:.2f}% → Tidak memenuhi syarat (≤ {batas_rpd}%)")

def tampilkan_kesimpulan_recovery(recovery):
    st.subheader("Kesimpulan Akurasi (%Recovery)")
    if recovery is None:
        st.info("Masukkan data spike yang valid")
        return
    batas_min, batas_max = 85, 115
    if batas_min <= recovery <= batas_max:
        st.success(f"%Recovery = {recovery:.2f}% → Memenuhi syarat ({batas_min}% - {batas_max}%)")
    else:
        st.error(f"%Recovery = {recovery:.2f}% → Tidak memenuhi syarat ({batas_min}% - {batas_max}%)")

# --- Main Program ---

st.sidebar.title("Menu Proses")
menu = st.sidebar.radio("Pilih Tahap:", [
    "Cover",
    "Input Data Standar",
    "Kurva Kalibrasi dan Hitung Konsentrasi Sampel",
    "Presisi (%RSD dan %RPD)",
    "Akurasi (%Recovery)"
])

if menu == "Cover":
    cover()

elif menu == "Input Data Standar":
    input_standards()

elif menu == "Kurva Kalibrasi dan Hitung Konsentrasi Sampel":
    if 'standar_df' not in st.session_state:
        st.warning("Masukkan data standar terlebih dahulu di menu 'Input Data Standar'.")
    else:
        df_standar = st.session_state['standar_df'].dropna()
        if len(df_standar) < 2:
            st.warning("Input minimal 2 data standar valid untuk kalibrasi.")
        else:
            intercept, slope, r2 = plot_kalibrasi(df_standar)
            st.markdown(f"Persamaan Kalibrasi: Absorbansi = {slope:.4f} × Konsentrasi + {intercept:.4f}")
            abs_sample = input_sample()
            if abs_sample >= 0:
                konsentrasi_sampel = hitung_konsentrasi(abs_sample, intercept, slope)
                st.write(f"*Konsentrasi sampel diperkirakan: {konsentrasi_sampel:.4f} ppm*")
                st.session_state['konsentrasi_sampel'] = konsentrasi_sampel

elif menu == "Presisi (%RSD dan %RPD)":
    konsentrasi_list = input_precision_data()
    if len(konsentrasi_list) < 2:
        st.info("Masukkan minimal 2 data pengukuran untuk presisi.")
    else:
        mean, std, rsd = hitung_rsd(konsentrasi_list)
        rpd = hitung_rpd(konsentrasi_list)
        st.write(f"Mean Konsentrasi: {mean:.4f} ppm")
        st.write(f"Std Dev: {std:.4f}")
        st.write(f"%RSD: {rsd:.2f}%")
        if rpd is not None:
            st.write(f"%RPD: {rpd:.2f}%")
        tampilkan_kesimpulan_rsd(rsd)
        tampilkan_kesimpulan_rpd(rpd)

elif menu == "Akurasi (%Recovery)":
    hasil_spike, hasil_asli, spike = input_recovery_data()
    recovery = hitung_recovery(hasil_spike, hasil_asli, spike)
    if recovery is not None:
        st.write(f"%Recovery: {recovery:.2f}%")
    tampilkan_kesimpulan_recovery(recovery)
