import streamlit as st
import pandas as pd
import joblib

from preprocessing import preprocess
from visualisasi import tampil_visualisasi

model = joblib.load(
    "model/model_nb_datasetneww.pkl"
)

tfidf = joblib.load(
    "model/tfidf_datasetneww.pkl"
)

def klasifikasi_dataset(df):

    st.subheader("Klasifikasi Dataset")


    kandidat = [

        "komentar",

        "comment",

        "text",

        "tweet",

        "isi"

    ]

    kolom = None

    for col in df.columns:

        if col.lower() in kandidat:

            kolom = col

            break

    if kolom is None:

        st.error(
            "Kolom komentar tidak ditemukan."
        )

        return

    st.write("Melakukan preprocessing...")

    df["preprocessing"] = (

        df[kolom]

        .astype(str)

        .apply(preprocess)

    )

    st.write("Membuat TF-IDF...")

    X = tfidf.transform(

        df["preprocessing"]

    )
    st.write("Melakukan klasifikasi...")

    hasil = model.predict(X)

    df["hasil"] = hasil

    st.success(
        "Prediksi selesai."
    )
    st.subheader("Hasil Prediksi")

    st.dataframe(df)
    tampil_visualisasi(df)
    csv = df.to_csv(index=False)

    st.download_button(

        "Download Hasil",
        csv,
        file_name="hasil_prediksi.csv",
        mime="text/csv"

    )