
import streamlit as st
import pandas as pd
import numpy as np

st.title("Kalkulator %RSD, %RPD, dan %Recovery")

st.write("""
Masukkan data Anda (pisahkan dengan koma atau upload file CSV):
""")

# Input data manual
data_input = st.text_area("Input Data (misal: 10, 12, 11, 13)", "")

# Input data lewat file
uploaded_file = st.file_uploader("Atau upload file CSV", type=["csv"])

data = []
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    data = df.iloc[:, 0].dropna().tolist()
elif data_input:
    try:
        data = [float(i) for i in data_input.replace(';', ',').split(',') if i.strip() != ""]
    except:
        st.error("Format data salah!")

if data:
    arr = np.array(data)
    mean = np.mean(arr)
    std = np.std(arr, ddof=1)
    rsd = (std / mean) * 100 if mean != 0 else 0

    st.write(f"*Mean:* {mean:.3f}")
    st.write(f"*Std Dev:* {std:.3f}")
    st.write(f"%RSD:** {rsd:.2f}%")

    if len(arr) == 2:
        rpd = (abs(arr[0] - arr[1]) / ((arr[0] + arr[1]) / 2)) * 100
        st.write(f"%RPD:** {rpd:.2f}%")
    else:
        st.info("Input dua data untuk menghitung %RPD.")

    # Recovery (butuh data hasil dan spike)
    st.write("### Hitung %Recovery")
    hasil = st.number_input("Hasil pengujian (hasil ditemukan)", value=0.0)
    spike = st.number_input("Nilai spike (nilai yang ditambahkan)", value=0.0)
    if spike != 0:
        recovery = (hasil / spike) * 100
        st.write(f"%Recovery:** {recovery:.2f}%")
else:
    st.info("Masukkan data terlebih dahulu.")
