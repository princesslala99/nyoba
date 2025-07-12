import streamlit as st
import pandas as pd
import numpy as np

st.title("Kalkulator Kimia Bertahap: %RSD, %RPD, dan %Recovery")

tab1, tab2, tab3 = st.tabs(["Input Data", "Perhitungan %RSD & %RPD", "Perhitungan %Recovery"])

with tab1:
    st.header("1. Input Data")
    data_input = st.text_area("Masukkan data (pisahkan dengan koma, misal: 10, 12, 11, 13)", "")
    uploaded_file = st.file_uploader("Atau upload file CSV", type=["csv"])
    data = []
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        data = df.iloc[:, 0].dropna().tolist()
        st.success("Data berhasil diupload!")
    elif data_input:
        try:
            data = [float(i) for i in data_input.replace(';', ',').split(',') if i.strip() != ""]
            st.success("Data berhasil dimasukkan!")
        except:
            st.error("Format data salah!")
    st.session_state['data'] = data

with tab2:
    st.header("2. Perhitungan %RSD & %RPD")
    data = st.session_state.get('data', [])
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
            st.info("Input dua data pada tab sebelumnya untuk menghitung %RPD.")
    else:
        st.info("Masukkan data terlebih dahulu di tab 'Input Data'.")

with tab3:
    st.header("3. Perhitungan %Recovery")
    hasil = st.number_input("Hasil pengujian (hasil ditemukan)", value=0.0)
    spike = st.number_input("Nilai spike (nilai yang ditambahkan)", value=0.0)
    if spike != 0:
        recovery = (hasil / spike) * 100
        st.write(f"%Recovery:** {recovery:.2f}%")
    else:
        st.info("Masukkan nilai spike lebih dari 0.")
