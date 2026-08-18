import hashlib
from pathlib import Path
from collections import Counter

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

from preprocessing import preprocess

from transformers import AutoTokenizer, AutoModelForSequenceClassification


# =========================================================
# KONFIGURASI MODEL
# =========================================================

NB_MODEL_PATH = "model/model_nb_datasetneww.pkl"
TFIDF_PATH = "model/tfidf_datasetneww.pkl"
INDOBERT_MODEL_PATH = "maszaidana/indoberttweet-sentimen-banjir"


# =========================================================
# SESSION STATE
# =========================================================

def init_upload_state():
    defaults = {
        "dataset_baru": None,
        "dataset_sudah_preprocessing": False,
        "dataset_terlabel": None,
        "komentar_column": None,
        "model_pilihan": None,
        "pilih_model": False,
        "file_signature": None,
        "file_name": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_dataset_state(signature=None, file_name=None):
    st.session_state.dataset_baru = None
    st.session_state.dataset_sudah_preprocessing = False
    st.session_state.dataset_terlabel = None
    st.session_state.komentar_column = None
    st.session_state.model_pilihan = None
    st.session_state.pilih_model = False
    st.session_state.file_signature = signature
    st.session_state.file_name = file_name


# =========================================================
# LOAD NAIVE BAYES
# =========================================================

@st.cache_resource

def load_nb_model():
    model = joblib.load(NB_MODEL_PATH)
    tfidf = joblib.load(TFIDF_PATH)
    return model, tfidf


# =========================================================
# LOAD INDOBERTWEET
# =========================================================

@st.cache_resource

def load_indobertweet():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(INDOBERT_MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(
        INDOBERT_MODEL_PATH
    )
    model.eval()

    return tokenizer, model


# =========================================================
# BACA DATASET
# =========================================================

def baca_dataset(file):
    ext = Path(file.name).suffix.lower()

    if ext == ".csv":
        return pd.read_csv(file)
    if ext == ".xlsx":
        return pd.read_excel(file)
    if ext == ".json":
        return pd.read_json(file)
    if ext in {".txt", ".tsv"}:
        return pd.read_csv(file, sep="\t")
    if ext == ".xml":
        return pd.read_xml(file)
    if ext == ".parquet":
        return pd.read_parquet(file)

    raise ValueError("Format file tidak didukung.")


def get_file_signature(file):
    return hashlib.md5(file.getvalue()).hexdigest()


# =========================================================
# DETEKSI KOLOM KOMENTAR
# =========================================================

def cari_kolom_komentar(df):
    kandidat = {
        "komentar",
        "comment",
        "text",
        "tweet",
        "isi",
        "review",
    }

    for col in df.columns:
        nama_colom = str(col).strip().lower()
        if nama_colom in kandidat:
            return col

    return None


# =========================================================
# WORDCLOUD
# =========================================================

def tampil_wordcloud(teks):
    teks = " ".join(
        str(x)
        for x in teks
        if pd.notna(x) and str(x).strip()
    )

    if not teks.strip():
        st.warning("Tidak terdapat kata yang dapat ditampilkan.")
        return

    wc = WordCloud(
        width=1200,
        height=500,
        background_color="white",
        colormap="viridis",
        max_words=100,
    ).generate(teks)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")

    st.pyplot(fig, width="stretch")
    plt.close(fig)


# =========================================================
# KATA TERBANYAK
# =========================================================

def kata_terbanyak(teks, jumlah=15):
    semua_kata = []

    for kalimat in teks:
        if pd.isna(kalimat):
            continue
        semua_kata.extend(str(kalimat).split())

    return Counter(semua_kata).most_common(jumlah)


# =========================================================
# INFORMASI MODEL
# =========================================================

def informasi_model(model):
    if model == "Naive Bayes":
        st.markdown(
            """
            <div class="algorithm-info nb-info">
                <div class="algorithm-icon">⚡</div>
                <div>
                    <h3>Naive Bayes</h3>
                    <p>
                        Naive Bayes merupakan algoritma klasifikasi
                        berbasis probabilitas yang relatif ringan
                        dan memiliki waktu komputasi yang lebih cepat.
                    </p>
                    <div class="algorithm-points">
                        ⚡ Komputasi relatif cepat<br>
                        💻 Ringan untuk dataset besar<br>
                        📊 Berbasis probabilitas<br>
                        📝 Menggunakan representasi TF-IDF
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif model == "IndoBERTweet":
        st.markdown(
            """
            <div class="algorithm-info bert-info">
                <div class="algorithm-icon">🤖</div>
                <div>
                    <h3>IndoBERTTweet</h3>
                    <p>
                        IndoBERTTweet merupakan model berbasis transformer
                        yang dirancang untuk memahami karakteristik bahasa
                        Indonesia pada data media sosial.
                    </p>
                    <div class="algorithm-points">
                        🧠 Memahami konteks bahasa<br>
                        🇮🇩 Bahasa Indonesia<br>
                        💬 Cocok untuk data media sosial<br>
                        ⏳ Komputasi relatif lebih tinggi <br>
                        🕑 Membutuhkan waktu sekitar 15-20 Menit
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# PREPROCESSING DATASET
# =========================================================

def jalankan_preprocessing(df, komentar_column):
    hasil_preprocessing = []
    total_data = len(df)

    if total_data == 0:
        return df.copy()

    progress = st.progress(0)
    status = st.empty()

    try:
        for i, komentar in enumerate(df[komentar_column]):
            # Jangan gunakan str(komentar) agar NaN tetap dapat
            # ditangani oleh fungsi preprocess().
            hasil = preprocess(komentar)
            hasil_preprocessing.append(hasil)

            progress.progress((i + 1) / total_data)
            status.write(
                f"Memproses data {i + 1:,} dari {total_data:,}..."
            )
    finally:
        progress.empty()
        status.empty()

    df_hasil = df.copy()
    df_hasil["preprocessing"] = hasil_preprocessing
    return df_hasil


# =========================================================
# KLASIFIKASI NAIVE BAYES
# =========================================================

def klasifikasi_naive_bayes(df):
    if "preprocessing" not in df.columns:
        raise ValueError(
            "Kolom 'preprocessing' belum tersedia. "
            "Jalankan preprocessing terlebih dahulu."
        )

    nb_model, tfidf = load_nb_model()
    teks = df["preprocessing"].fillna("").astype(str)

    progress = st.progress(0)
    status = st.empty()
    hasil = []

    try:
        total_data = len(teks)

        if total_data == 0:
            return df.copy()

        # Transform sekaligus lebih efisien daripada transform satu per satu.
        vector = tfidf.transform(teks.tolist())
        prediksi = nb_model.predict(vector)
        hasil = list(prediksi)

        progress.progress(1.0)
        status.write(f"Selesai mengklasifikasikan {total_data:,} data.")
    finally:
        progress.empty()
        status.empty()

    df_hasil = df.copy()
    df_hasil["hasil"] = hasil
    return df_hasil


# =========================================================
# KLASIFIKASI INDOBERTWEET
# =========================================================

def klasifikasi_indobertweet(df, komentar_column):
    import torch

    tokenizer, bert_model = load_indobertweet()
    hasil = []
    total_data = len(df)

    mapping = {
        0: "negatif",
        1: "netral",
        2: "positif",
    }

    progress = st.progress(0)
    status = st.empty()

    try:
        for i, komentar in enumerate(df[komentar_column]):
            teks = "" if pd.isna(komentar) else str(komentar)

            inputs = tokenizer(
                teks,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=256,
            )

            with torch.no_grad():
                outputs = bert_model(**inputs)

            prediksi = torch.argmax(outputs.logits, dim=1).item()

            # Mapping ini harus sesuai dengan label model saat training.
            if prediksi not in mapping:
                raise ValueError(
                    f"Label output IndoBERTweet tidak dikenal: {prediksi}"
                )

            hasil.append(mapping[prediksi])

            progress.progress((i + 1) / total_data)
            status.write(
                f"Mengklasifikasikan {i + 1:,} dari {total_data:,}..."
            )
    finally:
        progress.empty()
        status.empty()

    df_hasil = df.copy()
    df_hasil["hasil"] = hasil
    return df_hasil


# =========================================================
# KOMPONEN VISUAL HASIL
# =========================================================

def _sentiment_metrics(df):
    """Menghitung jumlah dan persentase setiap sentimen."""
    total = len(df)

    counts = df["hasil"].value_counts() if "hasil" in df.columns else {}

    positif = int(counts.get("positif", 0))
    netral = int(counts.get("netral", 0))
    negatif = int(counts.get("negatif", 0))

    def pct(value):
        return (value / total * 100) if total else 0

    return {
        "total": total,
        "positif": positif,
        "netral": netral,
        "negatif": negatif,
        "positif_pct": pct(positif),
        "netral_pct": pct(netral),
        "negatif_pct": pct(negatif),
    }


def _sentiment_card(icon, label, count, percentage, css_class):
    """Card statistik sentimen."""
    st.markdown(
        f"""
        <div class="sentiment-card {css_class}">
            <div class="sentiment-card-top">
                <div class="sentiment-emoji">{icon}</div>
                <div class="sentiment-percent">{percentage:.1f}%</div>
            </div>
            <div class="sentiment-label">{label}</div>
            <div class="sentiment-count">{count:,}</div>
            <div class="sentiment-caption">komentar</div>
            <div class="sentiment-progress">
                <div class="sentiment-progress-fill"
                     style="width:{min(max(percentage, 0), 100):.2f}%;">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _dominant_sentiment(metrics):
    """Mengembalikan sentimen dominan dan persentasenya."""
    values = {
        "Positif": metrics["positif_pct"],
        "Netral": metrics["netral_pct"],
        "Negatif": metrics["negatif_pct"],
    }

    dominant = max(values, key=values.get)

    return dominant, values[dominant]


# =========================================================
# TAMPILKAN HASIL KLASIFIKASI
# =========================================================

def tampilkan_hasil(df, model_pilihan):

    if df is None or "hasil" not in df.columns:
        return

    metrics = _sentiment_metrics(df)
    dominant, dominant_pct = _dominant_sentiment(metrics)

    # -----------------------------------------------------
    # HEADER HASIL
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="result-hero">
            <div class="result-hero-emoji">🎉</div>
            <div>
                <div class="result-hero-title">
                    Klasifikasi Selesai!
                </div>
                <div class="result-hero-subtitle">
                    Dataset berhasil dianalisis dan setiap komentar
                    telah diberikan label sentimen.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # MODEL + TOTAL DATA
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="result-meta">
            <span>🧠 Model: <b>{model_pilihan}</b></span>
            <span>📊 Total data: <b>{metrics["total"]:,}</b></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # SUMMARY CARDS
    # -----------------------------------------------------

    st.markdown("### 📊 Ringkasan Prediksi")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="total-card">
                <div class="summary-icon">📦</div>
                <div class="summary-label">Total Data</div>
                <div class="summary-number">
                    {metrics["total"]:,}
                </div>
                <div class="summary-caption">
                    komentar dianalisis
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        _sentiment_card(
            "😊",
            "Positif",
            metrics["positif"],
            metrics["positif_pct"],
            "positive-card",
        )

    with c3:
        _sentiment_card(
            "😐",
            "Netral",
            metrics["netral"],
            metrics["netral_pct"],
            "neutral-card",
        )

    with c4:
        _sentiment_card(
            "😡",
            "Negatif",
            metrics["negatif"],
            metrics["negatif_pct"],
            "negative-card",
        )

    # -----------------------------------------------------
    # DOMINAN SENTIMENT
    # -----------------------------------------------------

    dominant_icon = {
        "Positif": "😊",
        "Netral": "😐",
        "Negatif": "😡",
    }.get(dominant, "📊")

    st.markdown(
        f"""
        <div class="dominant-card">
            <div class="dominant-icon">{dominant_icon}</div>
            <div class="dominant-content">
                <div class="dominant-small">
                    SENTIMEN DOMINAN
                </div>
                <div class="dominant-title">
                    {dominant}
                </div>
                <div class="dominant-description">
                    Mendominasi <b>{dominant_pct:.1f}%</b>
                    dari seluruh {metrics["total"]:,} komentar
                    yang diprediksi.
                </div>
            </div>
            <div class="dominant-badge">
                {dominant_pct:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # GRAFIK DISTRIBUSI
    # -----------------------------------------------------

    st.markdown("### 📈 Distribusi Prediksi")

    chart = pd.DataFrame(
        {
            "Sentimen": ["Positif", "Netral", "Negatif"],
            "Jumlah": [
                metrics["positif"],
                metrics["netral"],
                metrics["negatif"],
            ],
            "Persentase": [
                metrics["positif_pct"],
                metrics["netral_pct"],
                metrics["negatif_pct"],
            ],
        }
    )

    kiri, kanan = st.columns([1, 1.15])

    with kiri:
        fig_pie = px.pie(
            chart,
            values="Jumlah",
            names="Sentimen",
            hole=0.62,
            color="Sentimen",
            color_discrete_map={
                "Positif": "#22C55E",
                "Netral": "#FACC15",
                "Negatif": "#EF4444",
            },
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Jumlah: %{value:,}<br>"
                "Persentase: %{percent}<extra></extra>"
            ),
        )

        fig_pie.update_layout(
            title={
                "text": "Proporsi Sentimen",
                "x": 0.02,
                "font": {"size": 18},
            },
            font_family="Poppins",
            margin=dict(l=10, r=10, t=55, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.12,
                xanchor="center",
                x=0.5,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig_pie,
            width="stretch",
            config={"displayModeBar": False},
        )

    with kanan:
        fig_bar = px.bar(
            chart,
            x="Sentimen",
            y="Jumlah",
            text="Jumlah",
            color="Sentimen",
            color_discrete_map={
                "Positif": "#22C55E",
                "Netral": "#FACC15",
                "Negatif": "#EF4444",
            },
        )

        fig_bar.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Jumlah: %{y:,}<extra></extra>"
            ),
        )

        fig_bar.update_layout(
            title={
                "text": "Jumlah Komentar",
                "x": 0.02,
                "font": {"size": 18},
            },
            font_family="Poppins",
            showlegend=False,
            margin=dict(l=10, r=10, t=55, b=10),
            yaxis_title="Jumlah komentar",
            xaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig_bar,
            width="stretch",
            config={"displayModeBar": False},
        )

    # -----------------------------------------------------
    # TABEL HASIL
    # -----------------------------------------------------

    with st.expander("📋 Lihat seluruh hasil klasifikasi", expanded=False):
        st.dataframe(
            df,
            width="stretch",
            height=420,
        )

    # -----------------------------------------------------
    # WORDCLOUD
    # -----------------------------------------------------

    if "preprocessing" in df.columns:

        st.divider()

        st.markdown("### ☁️ WordCloud Dataset")

        tampil_wordcloud(df["preprocessing"])

        # -------------------------------------------------
        # KATA TERBANYAK
        # -------------------------------------------------

        st.markdown("### 🔤 Kata yang Paling Banyak Muncul")

        top_words = kata_terbanyak(
            df["preprocessing"],
            15,
        )

        if top_words:

            kata_df = pd.DataFrame(
                top_words,
                columns=["Kata", "Frekuensi"],
            )

            st.dataframe(
                kata_df,
                width="stretch",
            )

        # -------------------------------------------------
        # KATA PER SENTIMEN
        # -------------------------------------------------

        st.markdown(
            "### 💬 Kata Terbanyak Berdasarkan Sentimen"
        )

        sentiment_tabs = st.tabs(
            ["😊 Positif", "😐 Netral", "😡 Negatif"]
        )

        for tab, label in zip(
            sentiment_tabs,
            ["positif", "netral", "negatif"],
        ):

            with tab:

                data_label = df.loc[
                    df["hasil"] == label,
                    "preprocessing",
                ]

                words = kata_terbanyak(
                    data_label,
                    10,
                )

                if not words:
                    st.info(
                        f"Belum ada data untuk sentimen {label}."
                    )
                    continue

                kata_df = pd.DataFrame(
                    words,
                    columns=["Kata", "Frekuensi"],
                )

                st.dataframe(
                    kata_df,
                    width="stretch",
                )

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.divider()

    output = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Hasil Klasifikasi",
        data=output,
        file_name="dataset_hasil_klasifikasi.csv",
        mime="text/csv",
        width="stretch",
    )


# =========================================================
# UPLOAD DATASET - UI UTAMA
# =========================================================

def upload_dataset():
    init_upload_state()

    # CSS untuk halaman ini sebaiknya diletakkan di style.py.
    # Jangan inject CSS berulang kali di dalam fungsi ini.

    st.markdown(
        """
        <div class="dataset-title">
            📂 Dataset
        </div>
        <div class="dataset-subtitle">
            Upload dataset komentar untuk dilakukan
            preprocessing dan klasifikasi sentimen secara otomatis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # STEP 1 - UPLOAD
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="process-card">
            <span class="process-number">1</span>
            <b>Masukkan Dataset</b>
            <br><br>
            Dataset baru dapat berupa file CSV, XLSX, JSON,
            TXT, TSV, XML, atau PARQUET.
        </div>
        """,
        unsafe_allow_html=True,
    )

    file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "json", "txt", "tsv", "xml", "parquet"],
        width="stretch",
    )

    if file is None:
        st.info(
            "📁 Silakan upload dataset terlebih dahulu. "
            "Tahap preprocessing dan klasifikasi akan aktif "
            "setelah dataset tersedia."
        )
        return

    # -----------------------------------------------------
    # DETEKSI FILE BARU
    # -----------------------------------------------------

    signature = get_file_signature(file)

    if st.session_state.file_signature != signature:
        reset_dataset_state(
            signature=signature,
            file_name=file.name,
        )

        try:
            file.seek(0)
            df = baca_dataset(file)
        except Exception as e:
            st.error(f"❌ Gagal membaca dataset: {e}")
            return

        if df is None or df.empty:
            st.warning("⚠️ Dataset kosong. Silakan upload dataset yang berisi data.")
            return

        df = df.reset_index(drop=True)

        komentar_column = cari_kolom_komentar(df)

        if komentar_column is None:
            st.error("❌ Kolom komentar tidak ditemukan.")
            st.write("Kolom yang tersedia:", list(df.columns))
            return

        st.session_state.dataset_baru = df
        st.session_state.komentar_column = komentar_column

    # Gunakan dataframe dari session state setelah file terdeteksi.
    df = st.session_state.dataset_baru
    komentar_column = st.session_state.komentar_column

    if df is None or komentar_column is None:
        st.error("❌ Dataset belum berhasil dipersiapkan.")
        return

    st.success(f"✅ Dataset **{file.name}** berhasil diunggah.")

    # -----------------------------------------------------
    # PREVIEW
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="process-card">
            <span class="process-number">2</span>
            <b>📄 Preview Dataset</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(df.head(10), width="stretch")

    st.success(
        f"💬 Kolom komentar terdeteksi: **{komentar_column}**"
    )

    # -----------------------------------------------------
    # PREPROCESSING
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="process-card">
            <span class="process-number">3</span>
            <b>⚙️ Preprocessing</b>
            <br><br>
            Dataset akan melalui cleaning, case folding,
            tokenizing, normalisasi slang, stopword removal,
            dan stemming.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.dataset_sudah_preprocessing:
        if st.button(
            "⚙️ Mulai Preprocessing",
            width="stretch",
            type="primary",
        ):
            try:
                df_hasil = jalankan_preprocessing(
                    df,
                    komentar_column,
                )
            except Exception as e:
                st.error(f"❌ Preprocessing gagal: {e}")
                return

            st.session_state.dataset_baru = df_hasil
            st.session_state.dataset_sudah_preprocessing = True

            st.success("✅ Preprocessing selesai.")
            st.rerun()

        return

    # Pastikan kolom preprocessing memang ada sebelum dipakai.
    if "preprocessing" not in df.columns:
        st.error(
            "❌ Kolom 'preprocessing' tidak ditemukan. "
            "Silakan jalankan preprocessing kembali."
        )
        st.session_state.dataset_sudah_preprocessing = False
        return

    st.success("🧹 Dataset telah selesai diproses.")

    st.dataframe(
        df[[komentar_column, "preprocessing"]],
        width="stretch",
        height=350,
    )

    # -----------------------------------------------------
    # PILIH MODEL
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="process-card">
            <span class="process-number">4</span>
            <b>🧠 Pemilihan Algoritma Klasifikasi</b>
            <br><br>
            Pilih algoritma yang akan digunakan untuk
            memberikan label sentimen secara otomatis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.pilih_model:
        if st.button(
            "🧠 Pilih Algoritma Klasifikasi",
            width="stretch",
            type="primary",
        ):
            st.session_state.pilih_model = True
            st.rerun()
        return

    model_pilihan = st.selectbox(
        "Pilih algoritma:",
        ["Naive Bayes", "IndoBERTweet"],
        index=(
            0
            if st.session_state.model_pilihan not in {
                "Naive Bayes",
                "IndoBERTweet",
            }
            else ["Naive Bayes", "IndoBERTweet"].index(
                st.session_state.model_pilihan
            )
        ),
    )

    st.session_state.model_pilihan = model_pilihan

    informasi_model(model_pilihan)

    st.warning(
        f"Algoritma yang dipilih: **{model_pilihan}**. "
        "Pastikan pilihan sudah sesuai sebelum memulai klasifikasi."
    )

    # -----------------------------------------------------
    # KLASIFIKASI
    # -----------------------------------------------------

    if st.button(
        "🚀 Lakukan Klasifikasi",
        width="stretch",
        type="primary",
    ):
        try:
            if model_pilihan == "Naive Bayes":
                df_hasil = klasifikasi_naive_bayes(df)
            else:
                df_hasil = klasifikasi_indobertweet(
                    df,
                    komentar_column,
                )
        except Exception as e:
            st.error(
                f"❌ Gagal menjalankan {model_pilihan}: {e}"
            )
            return

        st.session_state.dataset_terlabel = df_hasil
        st.session_state.dataset_baru = df_hasil

        st.success(
            "🎉 Klasifikasi selesai! Dataset berhasil diberikan label sentimen."
        )

        st.rerun()

    # -----------------------------------------------------
    # HASIL
    # -----------------------------------------------------

    df_hasil = st.session_state.dataset_terlabel

    if df_hasil is None:
        return

    tampilkan_hasil(
        df_hasil,
        model_pilihan,
    )