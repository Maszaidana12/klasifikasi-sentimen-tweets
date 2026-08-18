import streamlit as st
from streamlit_option_menu import option_menu

from dashboard import tampil_dashboard
from upload import upload_dataset
from analisis import analisis_komentar
from assets.style import load_css

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Analisis Sentimen",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# LOAD CSS
# ==================================================

load_css()


# ==================================================
# NAVBAR
# ==================================================

with st.container(key="navbar"):

    menu = option_menu(
        menu_title=None,

        options=[
            "Dashboard",
            "Dataset",
            #"Evaluasi",
            "Analisis",
            "Tentang"
        ],

        icons=[
            "house",
            "cloud-upload",
            "bar-chart",
            "chat",
            "info-circle"
        ],

        orientation="horizontal",

        default_index=0,

        styles={
            "container": {
                "padding": "0!important",
                "margin": "0!important",
                "background-color": "transparent",
                "border": "none",
            },

            "icon": {
                "font-size": "16px",
            },

            "nav-link": {
                "font-size": "14px",
                "font-family": "Poppins",
                "text-align": "center",
                "margin": "0px 4px",
                "padding": "10px 18px",
                "--hover-color": "#EFF6FF",
                "color": "#64748B",
            },

            "nav-link-selected": {
                "background-color": "#01467D",
                "color": "white",
                "font-weight": "600",
            },
        }
    )


# ==================================================
# HALAMAN
# ==================================================

if menu == "Dashboard":

    tampil_dashboard()


elif menu == "Dataset":

    upload_dataset()


#elif menu == "Evaluasi":

    #st.header("📈 Evaluasi Model")

    #st.info(
      #  "Halaman evaluasi model akan kita kembangkan."
    #)


elif menu == "Analisis":

    analisis_komentar()


elif menu == "Tentang":

    st.header("ℹ️ Tentang Aplikasi")

    st.write(
        """
        Aplikasi ini digunakan untuk melakukan
        analisis sentimen masyarakat terhadap
        respons pemerintah terkait isu banjir
        di Sumatera Tahun 2025.
        """
    )

