import streamlit as st
import numpy as np
import pandas as pd

st.title("Kalkulator Kimia Bertahap dengan Input Data Tabel")

tab1, tab2, tab3 = st.tabs(["1. Input Data", "2. Perhitungan %RSD & %RPD", "3. Perhitungan %Recovery"])

with tab1:
    st.header("Input Data dalam Bentuk Tabel")

    # Inisialisasi dataframe kosong dengan 5 baris default
    if 'data_df' not in st.session_state:
        st.session_state['data_df'] = pd.DataFrame({
            'Data': [np.nan]*5
        })

    # Editable data editor
    edited_df = st.data_editor(
        st.session_state['data_df'],
        num_rows="dynamic",
        use_container_width=True,
        key='data_editor'
    )

    # Simpan dataframe yang diedit ke session_state
    st.session_state['data_df'] = edited_df

    # Tampilkan data yang valid (non-null dan numeric)
    data = edited_df['Data'].dropna().tolist()
    if len(data) > 0:
        st.success(f"Data berhasil dimasukkan: {data}")
    else:
        st.info("Masukkan data minimal satu nilai.")

with tab2:
    st.header("Perhitungan %RSD & %RPD")
    data = st.session_state.get('data_df', pd.DataFrame()).dropna().squeeze()
    if isinstance(data, pd.Series):
        data_list = data.tolist()
    elif isinstance(data, list):
        data_list = data
    else:
        data_list = []

    if len(data_list) > 0:
        arr = np.array(data_list)
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
            st.info("Masukkan tepat dua data untuk menghitung %RPD.")
    else:
        st.info("Masukkan data terlebih dahulu di tab 'Input Data'.")

with tab3:
    st.header("Perhitungan %Recovery")
    hasil = st.number_input("Hasil pengujian (hasil ditemukan)", value=0.0)
    spike = st.number_input("Nilai spike (nilai yang ditambahkan)", value=0.0)
    if spike != 0:
        recovery = (hasil / spike) * 100
        st.write(f"%Recovery:** {recovery:.2f}%")
    else:
        st.info("Masukkan nilai spike lebih dari 0.")
