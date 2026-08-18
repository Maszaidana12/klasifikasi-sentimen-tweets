import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from wordcloud import WordCloud


def tampil_visualisasi(
    df,
    confusion_matrix=None,
    accuracy=None,
    precision=None,
    recall=None,
    f1=None
):

    st.divider()

    st.header("Dashboard Analisis Sentimen")

    # =====================================
    # HITUNG SENTIMEN
    # =====================================

    sentimen = df["hasil"].value_counts()

    positif = sentimen.get("positif", 0)
    netral = sentimen.get("netral", 0)
    negatif = sentimen.get("negatif", 0)

    total = len(df)

    # =====================================
    # METRIC
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Data", total)
    col2.metric("Positif", positif)
    col3.metric("Netral", netral)
    col4.metric("Negatif", negatif)

    st.divider()

    # =====================================
    # PIE CHART
    # =====================================

    st.subheader("Distribusi Sentimen")

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(

        [positif, netral, negatif],

        labels=[
            "Positif",
            "Netral",
            "Negatif"
        ],

        autopct="%1.1f%%",

        startangle=90

    )

    ax.axis("equal")

    st.pyplot(fig)

    # =====================================
    # BAR CHART
    # =====================================

    st.subheader("Grafik Batang")

    fig, ax = plt.subplots()

    ax.bar(

        [

            "Positif",

            "Netral",

            "Negatif"

        ],

        [

            positif,

            netral,

            negatif

        ]

    )

    st.pyplot(fig)

    # =====================================
    # WORD CLOUD
    # =====================================

    st.subheader("Word Cloud")

    teks = " ".join(
        df.iloc[:,0].astype(str)
    )

    wordcloud = WordCloud(

        width=800,

        height=400,

        background_color="white"

    ).generate(teks)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    ax.axis("off")

    st.pyplot(fig)

    # =====================================
    # CONFUSION MATRIX
    # =====================================

    if confusion_matrix is not None:

        st.divider()

        st.subheader("Confusion Matrix")

        cm = pd.DataFrame(confusion_matrix)

        st.dataframe(cm)

    # =====================================
    # METRIK
    # =====================================

    if accuracy is not None:

        st.divider()

        st.subheader("Evaluasi Model")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Accuracy",
            f"{accuracy:.2%}"
        )

        c2.metric(
            "Precision",
            f"{precision:.2%}"
        )

        c3.metric(
            "Recall",
            f"{recall:.2%}"
        )

        c4.metric(
            "F1 Score",
            f"{f1:.2%}"
        )

