import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from wordcloud import WordCloud
import matplotlib.pyplot as plt


# =========================================================
# FUNGSI UTAMA DASHBOARD
# =========================================================

def tampil_dashboard(df=None):

    # =====================================================
    # DATASET UTAMA
    # =====================================================

    if df is None:

        df = pd.read_excel(
            "data/dataset_stopword.xlsx"
        )

    # Pastikan data tidak kosong
    if df.empty:

        st.warning("Dataset kosong.")

        return


    # =====================================================
    # CSS DASHBOARD
    # =====================================================

    st.markdown(
        """
        <style>

        .dashboard-title {

            text-align: center;

            margin-top: 20px;

            margin-bottom: 8px;

            font-family: Poppins, sans-serif;

            font-size: 36px;

            font-weight: 700;

            color: #01467D;

        }


        .dashboard-subtitle {

            text-align: center;

            max-width: 800px;

            margin: 0 auto 35px auto;

            font-family: Poppins, sans-serif;

            font-size: 14px;

            line-height: 1.7;

            color: #64748B;

        }


        [data-testid="stMetric"] {

            background: #FFFFFF;

            padding: 20px;

            border-radius: 16px;

            border: 1px solid #E5E7EB;

            box-shadow:
                0 4px 15px rgba(0,0,0,0.04);

        }


        [data-testid="stMetricLabel"] {

            font-family: Poppins, sans-serif;

            font-size: 14px;

            color: #64748B;

        }


        [data-testid="stMetricValue"] {

            font-family: Poppins, sans-serif;

            font-size: 30px;

            font-weight: 700;

            color: #01467D;

        }


        .section-title {

            font-family: Poppins, sans-serif;

            font-size: 21px;

            font-weight: 700;

            color: #1E293B;

            margin-top: 25px;

            margin-bottom: 12px;

        }


        .result-card {

            background: #F8FAFC;

            border: 1px solid #E2E8F0;

            border-radius: 16px;

            padding: 20px;

            text-align: center;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        """
        <div class="dashboard-title">
            📊 Klasifikasi Sentimen
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="dashboard-subtitle">

        Visualisasi hasil analisis sentimen masyarakat
        terhadap respons pemerintah terkait isu penetapan
        status bencana nasional pada banjir di Sumatera
        Tahun 2025.

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # HITUNG DISTRIBUSI DATASET
    # =====================================================

    sentimen = df["Hasil"].value_counts()

    positif = sentimen.get("positif", 0)

    netral = sentimen.get("netral", 0)

    negatif = sentimen.get("negatif", 0)

    total = len(df)


    # =====================================================
    # METRIC DATASET UTAMA
    # =====================================================

    st.markdown(
        '<div class="section-title">📌 Distribusi Dataset Utama</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Data",
        total
    )


    col2.metric(
        "Positif",
        positif
    )


    col3.metric(
        "Netral",
        netral
    )


    col4.metric(
        "Negatif",
        negatif
    )


    # =====================================================
    # DATA CHART
    # =====================================================

    chart = pd.DataFrame({

        "Sentimen": [
            "Positif",
            "Netral",
            "Negatif"
        ],

        "Jumlah": [
            positif,
            netral,
            negatif
        ]

    })


    # =====================================================
    # PIE CHART
    # =====================================================

    fig = px.pie(

        chart,

        values="Jumlah",

        names="Sentimen",

        hole=0.50,

        color="Sentimen",

        color_discrete_map={

            "Positif": "#22C55E",

            "Netral": "#FACC15",

            "Negatif": "#EF4444"

        }

    )


    fig.update_traces(

        textposition="inside",

        textinfo="percent+label",

        hovertemplate=(
            "<b>%{label}</b><br>"
            "Jumlah: %{value}<br>"
            "Persentase: %{percent}"
            "<extra></extra>"
        )

    )


    fig.update_layout(

        title={
            "text": "Distribusi Sentimen",
            "x": 0.5,
            "xanchor": "center"
        },

        font_family="Poppins",

        showlegend=True

    )


    # =====================================================
    # BAR CHART
    # =====================================================

    fig_bar = px.bar(

        chart,

        x="Sentimen",

        y="Jumlah",

        text="Jumlah",

        color="Sentimen",

        color_discrete_map={

            "Positif": "#22C55E",

            "Netral": "#FACC15",

            "Negatif": "#EF4444"

        }

    )


    fig_bar.update_traces(

        textposition="outside"

    )


    fig_bar.update_layout(

        title={
            "text": "Jumlah Data Sentimen",
            "x": 0.5,
            "xanchor": "center"
        },

        font_family="Poppins",

        showlegend=False,

        xaxis_title="Sentimen",

        yaxis_title="Jumlah Data"

    )


    # =====================================================
    # TAMPILKAN CHART
    # =====================================================

    kiri, kanan = st.columns(2)


    with kiri:

        st.plotly_chart(

            fig,

            width="stretch",

            key="pie_dashboard"

        )


    with kanan:

        st.plotly_chart(

            fig_bar,

            width="stretch",

            key="bar_dashboard"

        )


    # =====================================================
    # WORDCLOUD KESELURUHAN
    # =====================================================

    st.markdown(
        '<div class="section-title">☁️ Wordcloud Dataset Utama</div>',
        unsafe_allow_html=True
    )


    if "preprocessing" in df.columns:

        teks_wordcloud = " ".join(
            df["preprocessing"]
            .dropna()
            .astype(str)
        )

    else:

        teks_wordcloud = " ".join(
            df["komentar"]
            .dropna()
            .astype(str)
        )


    if teks_wordcloud.strip():

        wordcloud = WordCloud(

            width=1200,

            height=500,

            background_color="white",

            max_words=100,

            collocations=False

        ).generate(teks_wordcloud)


        fig_wc, ax = plt.subplots(
            figsize=(14, 5)
        )


        ax.imshow(
            wordcloud,
            interpolation="bilinear"
        )


        ax.axis("off")


        st.pyplot(
            fig_wc,
            width="stretch"
        )


        plt.close(fig_wc)


    # =====================================================
    # KATA PALING BANYAK MUNCUL
    # =====================================================

    st.markdown(
        '<div class="section-title">🔤 Kata yang Paling Banyak Muncul</div>',
        unsafe_allow_html=True
    )


    if "preprocessing" in df.columns:

        teks = (
            df["preprocessing"]
            .dropna()
            .astype(str)
        )

    else:

        teks = (
            df["komentar"]
            .dropna()
            .astype(str)
        )


    vectorizer_count = CountVectorizer(

        max_features=20

    )


    X_count = vectorizer_count.fit_transform(
        teks
    )


    jumlah_kata = np.asarray(
        X_count.sum(axis=0)
    ).ravel()


    kata = vectorizer_count.get_feature_names_out()


    kata_df = pd.DataFrame({

        "Kata": kata,

        "Jumlah": jumlah_kata

    }).sort_values(

        "Jumlah",

        ascending=False

    ).head(10)


    fig_kata = px.bar(

        kata_df.sort_values(
            "Jumlah",
            ascending=True
        ),

        x="Jumlah",

        y="Kata",

        orientation="h",

        text="Jumlah",

        title="10 Kata dengan Frekuensi Tertinggi"

    )


    fig_kata.update_layout(

        font_family="Poppins",

        yaxis_title="Kata",

        xaxis_title="Frekuensi"

    )


    st.plotly_chart(

        fig_kata,

        width="stretch",

        key="kata_terbanyak"

    )


    # =====================================================
    # KATA TERBANYAK BERDASARKAN SENTIMEN
    # =====================================================

    st.markdown(
        '<div class="section-title">🔎 Kata Terbanyak Berdasarkan Kelas Sentimen</div>',
        unsafe_allow_html=True
    )


    sentimen_list = [
        "positif",
        "netral",
        "negatif"
    ]


    cols = st.columns(3)


    for col, label in zip(
        cols,
        sentimen_list
    ):

        data_kelas = df[
            df["Hasil"].str.lower() == label
        ]


        if len(data_kelas) == 0:

            col.info(
                f"Tidak ada data {label}."
            )

            continue


        if "preprocessing" in data_kelas.columns:

            teks_kelas = (
                data_kelas["preprocessing"]
                .dropna()
                .astype(str)
            )

        else:

            teks_kelas = (
                data_kelas["komentar"]
                .dropna()
                .astype(str)
            )


        vectorizer_kelas = CountVectorizer(
            max_features=5
        )


        X_kelas = vectorizer_kelas.fit_transform(
            teks_kelas
        )


        jumlah_kelas = np.asarray(
            X_kelas.sum(axis=0)
        ).ravel()


        kata_kelas = (
            vectorizer_kelas
            .get_feature_names_out()
        )


        hasil_kelas = pd.DataFrame({

            "Kata": kata_kelas,

            "Jumlah": jumlah_kelas

        }).sort_values(

            "Jumlah",

            ascending=False

        )


        col.markdown(
            f"**{label.capitalize()}**"
        )


        col.dataframe(

            hasil_kelas,

            hide_index=True,

            width="stretch"

        )


    # =====================================================
    # EVALUASI NAIVE BAYES
    # =====================================================

    st.divider()


    st.markdown(
        '<div class="section-title">🧠 Implementasi Naive Bayes pada Data Testing</div>',
        unsafe_allow_html=True
    )


    st.write(
        """
        Dataset utama dibagi menjadi data training dan data testing
        dengan perbandingan 80:20. Data training digunakan untuk
        membentuk model Naive Bayes, sedangkan data testing digunakan
        untuk mengukur kemampuan model dalam melakukan klasifikasi
        terhadap data yang belum digunakan pada proses pelatihan.
        """
    )


    # =====================================================
    # CARI KOLOM TEKS HASIL PREPROCESSING
    # =====================================================

    kandidat_preprocessing = [
        "preprocessing",
        "hasil_preprocessing",
        "komentar_preprocessing",
        "komentar_tokenized",
        "stemming",
        "hasil_stemming",
        "text_clean",
        "clean_text"
    ]

    kolom_preprocessing = None

    for col in df.columns:

        if col.lower().strip() in kandidat_preprocessing:

            kolom_preprocessing = col

            break


    # =====================================================
    # JIKA TIDAK DITEMUKAN
    # =====================================================

    if kolom_preprocessing is None:

        st.warning(
            "⚠️ Kolom hasil preprocessing tidak ditemukan."
        )

        st.write(
            "Kolom yang tersedia pada dataset:"
        )

        st.write(
            list(df.columns)
        )

        st.info(
            """
            Pastikan dataset utama memiliki kolom teks
            yang sudah melalui tahap preprocessing.
            """
        )

        return


    st.success(
        f"✅ Kolom preprocessing yang digunakan: **{kolom_preprocessing}**"
    )


    # =====================================================
    # DATA UNTUK MODEL
    # =====================================================

    X = (
        df[kolom_preprocessing]
        .fillna("")
        .astype(str)
    )

    y = (
        df["Hasil"]
        .fillna("")
        .astype(str)
    )



    # Hilangkan data kosong

    valid = X.str.strip() != ""

    X = X[valid]

    y = y[valid]


    # =====================================================
    # SPLIT 80 : 20
    # =====================================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=78,

        stratify=y

    )


    # =====================================================
    # TF-IDF
    # =====================================================

    tfidf = TfidfVectorizer(

        max_features=2000,

        min_df=3,

        max_df=0.9,

        ngram_range=(1, 2)

    )


    X_train_tfidf = tfidf.fit_transform(
        X_train
    )


    X_test_tfidf = tfidf.transform(
        X_test
    )


    # =====================================================
    # MODEL NAIVE BAYES
    # =====================================================

    model = MultinomialNB(

        alpha=0.5,

        fit_prior=True

    )


    model.fit(

        X_train_tfidf,

        y_train

    )


    # =====================================================
    # PREDIKSI DATA TESTING
    # =====================================================

    y_pred = model.predict(

        X_test_tfidf

    )


    # =====================================================
    # METRIC
    # =====================================================

    accuracy = accuracy_score(

        y_test,

        y_pred

    )


    precision = precision_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0

    )


    recall = recall_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0

    )


    f1 = f1_score(

        y_test,

        y_pred,

        average="weighted",

        zero_division=0

    )


    # =====================================================
    # TAMPILKAN METRIC TESTING
    # =====================================================

    st.markdown(
        "### 📈 Hasil Evaluasi Data Testing"
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Akurasi",
        f"{accuracy * 100:.2f}%"
    )


    c2.metric(
        "Precision",
        f"{precision * 100:.2f}%"
    )


    c3.metric(
        "Recall",
        f"{recall * 100:.2f}%"
    )


    c4.metric(
        "F1-Score",
        f"{f1 * 100:.2f}%"
    )


    # =====================================================
    # INFORMASI DATA
    # =====================================================

    st.info(

        f"""
        Dataset terdiri dari **{len(df)} data**.

        Sebanyak **{len(X_train)} data**
        digunakan sebagai data training dan
        **{len(X_test)} data** digunakan sebagai data testing.

        Berdasarkan data testing, model Naive Bayes
        memperoleh akurasi sebesar
        **{accuracy * 100:.2f}%**.
        """

    )


    # =====================================================
    # CONFUSION MATRIX
    # =====================================================

    st.markdown(
        "### 🔲 Confusion Matrix"
    )


    labels = [
        "negatif",
        "netral",
        "positif"
    ]


    cm = confusion_matrix(

        y_test,

        y_pred,

        labels=labels

    )


    fig_cm = px.imshow(

        cm,

        x=labels,

        y=labels,

        text_auto=True,

        color_continuous_scale="Blues",

        labels={
            "x": "Prediksi",
            "y": "Label Aktual",
            "color": "Jumlah"
        }

    )


    fig_cm.update_layout(

        title={
            "text": "Confusion Matrix Naive Bayes",
            "x": 0.5
        },

        font_family="Poppins"

    )


    st.plotly_chart(

        fig_cm,

        width="stretch",

        key="confusion_matrix"

    )

    st.markdown(
            '<div class="section-title">☁️ Wordcloud Data Testing </div>',
            unsafe_allow_html=True
        )
    
    
    if "preprocessing" in df.columns:
    
            teks_wordcloud = " ".join(
                df["Teks"]
                .dropna()
                .astype(str)
            )
    
    else:
    
            teks_wordcloud = " ".join(
                df["komentar"]
                .dropna()
                .astype(str)
            )
    
    
    if teks_wordcloud.strip():
    
            wordcloud = WordCloud(
    
                width=1200,
    
                height=500,
    
                background_color="white",
    
                max_words=100,
    
                collocations=False
    
            ).generate(teks_wordcloud)
    
    
            fig_wc, ax = plt.subplots(
                figsize=(14, 5)
            )
    
    
            ax.imshow(
                wordcloud,
                interpolation="bilinear"
            )
    
    
            ax.axis("off")
    
    
            st.pyplot(
                fig_wc,
                width="stretch"
            )
    
    
            plt.close(fig_wc)


    # =====================================================
    # CLASSIFICATION REPORT
    # =====================================================

    st.markdown(
        "### 📋 Classification Report"
    )


    report = classification_report(

        y_test,

        y_pred,

        labels=labels,

        output_dict=True,

        zero_division=0

    )

    report_df = pd.DataFrame(
        report
    ).transpose()


    st.dataframe(

        report_df.round(3),

        width="stretch"

    )


    # =====================================================
    # DISTRIBUSI HASIL PREDIKSI TESTING
    # =====================================================

    st.markdown(
        "### 📊 Distribusi Prediksi Data Testing"
    )


    prediksi_count = pd.Series(
        y_pred
    ).value_counts()


    prediksi_chart = pd.DataFrame({

        "Sentimen": prediksi_count.index,

        "Jumlah": prediksi_count.values

    })


    fig_pred = px.bar(

        prediksi_chart,

        x="Sentimen",

        y="Jumlah",

        text="Jumlah",

        color="Sentimen",

        color_discrete_map={

            "positif": "#22C55E",

            "netral": "#FACC15",

            "negatif": "#EF4444"

        },

        title="Distribusi Prediksi Sentimen Data Testing"

    )


    fig_pred.update_traces(

        textposition="outside"

    )


    fig_pred.update_layout(

        font_family="Poppins",

        showlegend=False

    )


    st.plotly_chart(

        fig_pred,

        width="stretch",

        key="prediksi_testing"

    )


    # =====================================================
    # PREDIKSI PALING DOMINAN
    # =====================================================

    prediksi_dominan = (
        pd.Series(y_pred)
        .value_counts()
        .idxmax()
    )


    jumlah_prediksi_dominan = (
        pd.Series(y_pred)
        .value_counts()
        .max()
    )


    persen_prediksi_dominan = (

        jumlah_prediksi_dominan
        /
        len(y_pred)

    ) * 100


    # =====================================================
    # PREDIKSI BENAR
    # =====================================================

    benar = np.sum(

        np.array(y_test)
        ==
        np.array(y_pred)

    )


    salah = len(y_test) - benar


    # =====================================================
    # KESIMPULAN TESTING
    # =====================================================

    st.markdown(
        "### 📌 Kesimpulan Hasil Testing"
    )


    st.info(

        f"""
        Berdasarkan hasil pengujian terhadap
        **{len(y_test)} data testing**, model
        Naive Bayes memperoleh akurasi sebesar
        **{accuracy * 100:.2f}%**.

        Dari seluruh data testing tersebut,
        sebanyak **{benar} data** berhasil
        diklasifikasikan sesuai dengan label aktual,
        sedangkan **{salah} data** mengalami kesalahan
        klasifikasi.

        Berdasarkan hasil prediksi model,
        kelas sentimen **{prediksi_dominan}**
        merupakan kelas yang paling dominan,
        yaitu sebanyak **{jumlah_prediksi_dominan} data**
        atau sekitar **{persen_prediksi_dominan:.2f}%**
        dari keseluruhan data testing.
        """

    )


    # =====================================================
    # DATA TESTING
    # =====================================================

    st.markdown(
        "### 📄 Hasil Prediksi Data Testing"
    )


    hasil_testing = pd.DataFrame({

        "Teks": X_test.values,

        "Label Aktual": y_test.values,

        "Label Prediksi": y_pred

    })


    hasil_testing["Status"] = np.where(

        hasil_testing["Label Aktual"]
        ==
        hasil_testing["Label Prediksi"],

        "Benar",

        "Salah"

    )


    st.dataframe(

        hasil_testing,

        width="stretch",

        height=400

    )


    # =====================================================
    # DATASET UTAMA
    # =====================================================

    st.divider()


    st.markdown(
        '<div class="section-title">📄 Dataset Utama</div>',
        unsafe_allow_html=True
    )


    st.dataframe(

        df,

        width="stretch",

        height=400

    )