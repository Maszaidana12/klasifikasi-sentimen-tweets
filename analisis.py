import streamlit as st
import joblib

from preprocessing import preprocess


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(
    "model/model_nb_datasetneww.pkl"
)

tfidf = joblib.load(
    "model/tfidf_datasetneww.pkl"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .analysis-title {
        font-size: 30px;
        font-weight: 700;
        color: #01467D;
        margin-bottom: 5px;
    }

    .analysis-subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .result-card {
        padding: 22px;
        border-radius: 16px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        margin-top: 15px;
    }

    .result-title {
        font-size: 18px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 15px;
    }

    .prediction-box {
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-top: 15px;
    }

    .prediction-label {
        font-size: 26px;
        font-weight: 700;
        margin-top: 5px;
    }

    .probability-label {
        font-size: 14px;
        font-weight: 600;
        color: #334155;
        margin-bottom: 5px;
    }

    .example-text {
        padding: 12px 15px;
        border-radius: 10px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 8px;
        color: #334155;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="analysis-title">
        💬 Analisis Komentar
    </div>

    <div class="analysis-subtitle">
        Masukkan komentar untuk melihat proses preprocessing,
        hasil klasifikasi sentimen, dan tingkat probabilitas
        pada masing-masing kelas sentimen.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CONTOH KOMENTAR
# =========================================================
def analisis_komentar():
    st.markdown(
        "### 💡 Contoh Komentar"
    )

    st.caption(
        "Pilih salah satu contoh berikut atau masukkan komentar sendiri."
    )

    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "😊 Contoh Positif",
            use_container_width=True
        ):

            st.session_state["komentar_analisis"] = (
                "Masya Allah relawan dan donasi sudah banyak berdatangan membantu "
                "masyarakat"
            )


    with col2:

        if st.button(
            "😐 Contoh Netral",
            use_container_width=True
        ):

            st.session_state["komentar_analisis"] = (
                "Banjir terjadi di beberapa wilayah "
                "Sumatera setelah hujan deras"
            )


    with col3:

        if st.button(
            "😡 Contoh Negatif",
            use_container_width=True
        ):

            st.session_state["komentar_analisis"] = (
                "Pemerintah tidak becus menangani "
                "masalah banjir"
            )


    # =========================================================
    # TEXT AREA
    # =========================================================

    komentar = st.text_area(
        "Masukkan komentar",
        value=st.session_state.get(
            "komentar_analisis",
            ""
        ),
        height=120,
        placeholder="Contoh: Pemerintah sudah membantu masyarakat korban banjir..."
    )


    # =========================================================
    # BUTTON ANALISIS
    # =========================================================

    if st.button(
        "🔍 Analisis Sentimen",
        type="primary",
        use_container_width=True
    ):

        if not komentar.strip():

            st.warning(
                "⚠️ Masukkan komentar terlebih dahulu."
            )

            st.stop()


        # =====================================================
        # PREPROCESSING
        # =====================================================

        hasil_preprocessing = preprocess(
            komentar
        )


        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-title">🧹 Hasil Preprocessing</div>',
            unsafe_allow_html=True
        )

        st.code(
            hasil_preprocessing,
            language="text"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # =====================================================
        # TF-IDF
        # =====================================================

        vector = tfidf.transform(
            [hasil_preprocessing]
        )


        # =====================================================
        # PREDIKSI
        # =====================================================

        hasil = model.predict(
            vector
        )[0]


        # =====================================================
        # PROBABILITAS
        # =====================================================

        probabilitas = model.predict_proba(
            vector
        )[0]

        kelas = model.classes_


        probabilitas_dict = dict(
            zip(
                kelas,
                probabilitas
            )
        )


        # =====================================================
        # HASIL UTAMA
        # =====================================================

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-title">🎯 Hasil Analisis Sentimen</div>',
            unsafe_allow_html=True
        )


        if hasil == "positif":

            st.success(
                "😊 Komentar diklasifikasikan sebagai SENTIMEN POSITIF"
            )

        elif hasil == "netral":

            st.info(
                "😐 Komentar diklasifikasikan sebagai SENTIMEN NETRAL"
            )

        else:

            st.error(
                "😡 Komentar diklasifikasikan sebagai SENTIMEN NEGATIF"
            )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # =====================================================
        # PROBABILITAS
        # =====================================================

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📊 Tingkat Keyakinan Model"
        )

        st.caption(
            "Nilai menunjukkan probabilitas model terhadap setiap kelas sentimen."
        )


        # -----------------------------------------------------
        # POSITIF
        # -----------------------------------------------------

        positif_prob = probabilitas_dict.get(
            "positif",
            0
        )

        st.markdown(
            f"**😊 Positif — {positif_prob * 100:.2f}%**"
        )

        st.progress(
            float(positif_prob)
        )


        # -----------------------------------------------------
        # NETRAL
        # -----------------------------------------------------

        netral_prob = probabilitas_dict.get(
            "netral",
            0
        )

        st.markdown(
            f"**😐 Netral — {netral_prob * 100:.2f}%**"
        )

        st.progress(
            float(netral_prob)
        )


        # -----------------------------------------------------
        # NEGATIF
        # -----------------------------------------------------

        negatif_prob = probabilitas_dict.get(
            "negatif",
            0
        )

        st.markdown(
            f"**😡 Negatif — {negatif_prob * 100:.2f}%**"
        )

        st.progress(
            float(negatif_prob)
        )


        # =====================================================
        # KESIMPULAN
        # =====================================================

        probabilitas_tertinggi = max(
            probabilitas_dict.values()
        )

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        st.info(
            f"""
            ### 📌 Kesimpulan Analisis

            Berdasarkan hasil klasifikasi, komentar tersebut
            termasuk dalam kelas sentimen **{hasil.upper()}**
            dengan tingkat probabilitas sebesar
            **{probabilitas_tertinggi * 100:.2f}%**.

            Model membandingkan probabilitas terhadap tiga kelas
            sentimen, yaitu positif, netral, dan negatif.
            Kelas dengan probabilitas tertinggi ditetapkan sebagai
            hasil klasifikasi komentar.
            """
        )