import streamlit as st
import pandas as pd
import numpy as np

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
    rsd =
