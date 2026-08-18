import streamlit as st
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from sklearn.naive_bayes import MultinomialNB

from preprocessing import preprocess
from visualisasi import tampil_visualisasi

def training_dataset(df):

    st.subheadr("Training Dataset Baru")

    kandidat_komentar = [
      "komentar",
      "comment",
      "tweets",
      "text",
      "teks",
      "isi",
    ]

    kandidat_label = [
        "hasil",
        "sentimen",
        "label",
        "kelas"
    ]

    kolom_komentar = None
    kolom_label = None

    for col in df.columns:

        if col.lower() in kandidat_komentar:
            kolom_komentar = col

        if col.lower() in kandidat_label:
            kolom_label = col

    if kolom_komentar is None:

        st.error("Kolom komentar tidak ditemukan")
        return

    if kolom_label is None:

        st.error("kolom label tidak ditemukan")
        return

    st.write("Melakukan Preprocessing....")

    df[kolom_komentar]=(
        df[kolom_komentar]
        .astype(str)
        .apply(preprocess)
    )

    tfidf = joblib.load("model/tf-idf.pkl")
    X = tfidf.fit_transform(
        df[kolom_komentar]
    )
    y = df[kolom_label]

    # SPLITTING

    pilihan = st.selectbox(

        "Pembagian Data(Spliting Data)"

        [
            "50:50",
            "60:40",
            "70:30",
            "80:20",
            "90:10"
        ]
    )

    mapping ={
        "50:50":0.5,
        "60:40":0.4,
        "70:30":0.3,
        "80:20":0.2,
        "90:10":0.1
    }

    test_size = mapping[pilihan]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,

        test_size = test_size,
        random_state = 78,
        stratify = y
    )

    st.success("Spliting Selesai")

    model = MultinomialNB(
        alpha = 0.5,
        fit_prior = True
    )

    model.fit(
        X_train,
        y_train
    )
    prediksi = model.predict(
        X_test
    )

    akurasi = accuracy_score(
        y_test,
        prediksi
    )
    precision = precision_score(
        y_test,
        prediksi,
        average="weighted"
    )
    recall = recall_score(

        y_test,
        prediksi,
        average="weighted"
    )
    f1 = f1_score(
        y_test,
        prediksi,
        average="weighted"
    )
    cm = confusion_matrix (
        y_test,
        prediksi
    )

    st.divider()
    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Accuracy",
        f"{akurasi:.2%}"
    )
    col2.metric(
        "Precision",
        f"{precision:.2%}"
    )
    col.metric(
        "Recall",
        f"{recall:.2%}"
    )
    col.metric(
        "F1-Score",
        f"{f1:.2%}"
    )

    tampil_visualisasi(
        df,
        confusion_matrix=cm,
       accuracy=akurasi,
        precision=precision,
        recall=recall,
        f1=f1
    )
