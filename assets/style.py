
import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* ==================================================
           GLOBAL
        ================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap'
        );

        html,
        body,
        [class*="css"],
        .stApp {
            font-family: 'Poppins', sans-serif;
        }


        /* ==================================================
           HEADER STREAMLIT
        ================================================== */

        header[data-testid="stHeader"] {
            display: none;
        }


        /* ==================================================
           BACKGROUND
        ================================================== */

        .stApp {
            background-color: #F4F7FC;
        }


        /* ==================================================
           NAVBAR FLOATING
        ================================================== */

        .st-key-navbar {

            position: fixed !important;

            top: 18px !important;

            left: 50% !important;

            transform: translateX(-50%) !important;

            width: calc(100% - 100px) !important;

            max-width: 1200px !important;

            z-index: 999999 !important;

            background: rgba(255, 255, 255, 0.96) !important;

            backdrop-filter: blur(12px);

            -webkit-backdrop-filter: blur(12px);

            border: 1px solid #E2E8F0;

            border-radius: 16px;

            padding: 8px 12px;

            box-shadow:
                0 8px 25px rgba(15, 23, 42, 0.08);

        }


        /* ==================================================
           OPTION MENU
        ================================================== */

        .st-key-navbar ul.nav.nav-pills {

            display: flex !important;

            align-items: center;

            width: 100%;

            gap: 4px;

        }


        .st-key-navbar .nav-link {

            font-family: 'Poppins', sans-serif !important;

            font-size: 14px !important;

            font-weight: 500 !important;

            border-radius: 10px !important;

            color: #64748B !important;

            transition: all 0.2s ease;

        }


        .st-key-navbar .nav-link:hover {

            background-color: #EFF6FF !important;

            color: #01467D !important;

        }


        .st-key-navbar .nav-link.active {

            background-color: #01467D !important;

            color: white !important;

            font-weight: 600 !important;

        }


        /* ==================================================
           KONTEN
        ================================================== */

        .block-container {

            padding-top: 115px !important;

            padding-bottom: 50px !important;

            max-width: 1400px !important;

        }


        /* ==================================================
           GENERAL CARD
        ================================================== */

        .card {

            background: white;

            padding: 25px;

            border-radius: 20px;

            box-shadow:
                0 8px 20px rgba(0, 0, 0, .08);

            margin-bottom: 20px;

        }


        /* ==================================================
           MODEL CARD
        ================================================== */

        .model-card {

            background: white;

            padding: 28px;

            border-radius: 20px;

            min-height: 280px;

            box-shadow:
                0 8px 20px rgba(0, 0, 0, .08);

            border: 1px solid #E8EDF5;

            margin-bottom: 20px;

        }

        .model-icon {

            font-size: 38px;

            margin-bottom: 15px;

        }

        .model-card h3 {

            color: #01467D;

            font-size: 24px;

            font-weight: 600;

            margin-bottom: 12px;

        }

        .model-card p {

            color: #666;

            font-size: 15px;

            line-height: 1.7;

            margin-bottom: 20px;

        }

        .model-info {

            color: #444;

            font-size: 14px;

            line-height: 2;

        }


        /* ==================================================
           MODEL INFORMATION
        ================================================== */

        .algorithm-info {

            display: flex;

            align-items: flex-start;

            gap: 18px;

            padding: 24px;

            border-radius: 20px;

            margin: 15px 0 20px 0;

            background: white;

            border: 1px solid #E8EDF5;

            box-shadow:
                0 9px 24px rgba(0, 0, 0, .055);

            animation:
                fadeUp .45s ease both;

        }

        .algorithm-icon {

            flex: 0 0 58px;

            width: 58px;

            height: 58px;

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 17px;

            font-size: 29px;

            background: #EAF3FA;

        }

        .algorithm-info h3 {

            margin: 0 0 7px 0;

            color: #01467D;

            font-size: 22px;

            font-weight: 700;

        }

        .algorithm-info p {

            margin: 0 0 12px 0;

            color: #667085;

            font-size: 14px;

            line-height: 1.7;

        }

        .algorithm-points {

            color: #3F4B5A;

            font-size: 13px;

            line-height: 1.9;

        }

        .nb-info {

            border-left: 5px solid #01467D;

        }

        .bert-info {

            border-left: 5px solid #7C3AED;

        }

        .bert-info .algorithm-icon {

            background: #F2ECFF;

        }


        /* ==================================================
           RESULT HERO
        ================================================== */

        .result-hero {

            display: flex;

            align-items: center;

            gap: 18px;

            padding: 24px 26px;

            margin: 10px 0 12px 0;

            border-radius: 22px;

            background:
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #F2F8FD 100%
                );

            border: 1px solid #DCE9F5;

            box-shadow:
                0 12px 28px rgba(1, 70, 125, .07);

            animation:
                resultEnter .55s ease both;

        }

        .result-hero-emoji {

            font-size: 46px;

            animation:
                emojiBounce 1.5s ease-in-out infinite;

        }

        .result-hero-title {

            color: #01467D;

            font-size: 28px;

            font-weight: 700;

        }

        .result-hero-subtitle {

            color: #667085;

            font-size: 14px;

            margin-top: 4px;

        }


        /* ==================================================
           RESULT META
        ================================================== */

        .result-meta {

            display: flex;

            gap: 10px;

            flex-wrap: wrap;

            margin: 10px 0 22px 0;

        }

        .result-meta span {

            display: inline-block;

            padding: 8px 13px;

            border-radius: 999px;

            background: #EAF3FA;

            color: #31506A;

            font-size: 13px;

        }


        /* ==================================================
           TOTAL & SENTIMENT CARD
        ================================================== */

        .total-card,
        .sentiment-card {

            min-height: 172px;

            padding: 20px;

            border-radius: 20px;

            background: white;

            border: 1px solid #E7EDF5;

            box-shadow:
                0 9px 24px rgba(0, 32, 74, .055);

            transition:
                transform .25s ease,
                box-shadow .25s ease;

            animation:
                fadeUp .5s ease both;

        }


        .total-card:hover,
        .sentiment-card:hover {

            transform: translateY(-4px);

            box-shadow:
                0 15px 30px rgba(0, 32, 74, .10);

        }


        .summary-icon {

            font-size: 28px;

            margin-bottom: 7px;

        }

        .summary-label,
        .sentiment-label {

            color: #667085;

            font-size: 13px;

            font-weight: 600;

        }

        .summary-number,
        .sentiment-count {

            color: #01467D;

            font-size: 28px;

            font-weight: 700;

            margin-top: 3px;

        }

        .summary-caption,
        .sentiment-caption {

            color: #98A2B3;

            font-size: 12px;

        }


        /* ==================================================
           SENTIMENT CARD TOP
        ================================================== */

        .sentiment-card-top {

            display: flex;

            align-items: center;

            justify-content: space-between;

        }

        .sentiment-emoji {

            font-size: 28px;

        }

        .sentiment-percent {

            font-size: 18px;

            font-weight: 700;

        }


        /* POSITIF */

        .positive-card {

            border-top: 4px solid #22C55E;

        }

        .positive-card .sentiment-percent {

            color: #16A34A;

        }


        /* NETRAL */

        .neutral-card {

            border-top: 4px solid #FACC15;

        }

        .neutral-card .sentiment-percent {

            color: #CA8A04;

        }


        /* NEGATIF */

        .negative-card {

            border-top: 4px solid #EF4444;

        }

        .negative-card .sentiment-percent {

            color: #DC2626;

        }


        /* ==================================================
           PROGRESS
        ================================================== */

        .sentiment-progress {

            height: 7px;

            margin-top: 12px;

            overflow: hidden;

            border-radius: 99px;

            background: #EEF2F6;

        }

        .sentiment-progress-fill {

            height: 100%;

            border-radius: 99px;

            transform-origin: left center;

            animation:
                progressGrow 1s ease both;

        }

        .positive-card .sentiment-progress-fill {

            background: #22C55E;

        }

        .neutral-card .sentiment-progress-fill {

            background: #FACC15;

        }

        .negative-card .sentiment-progress-fill {

            background: #EF4444;

        }


        /* ==================================================
           DOMINANT SENTIMENT
        ================================================== */

        .dominant-card {

            display: flex;

            align-items: center;

            gap: 17px;

            padding: 20px 23px;

            margin: 20px 0 25px 0;

            border-radius: 20px;

            background: white;

            border: 1px solid #E7EDF5;

            box-shadow:
                0 9px 24px rgba(0, 32, 74, .055);

            animation:
                fadeUp .6s ease both;

        }

        .dominant-icon {

            width: 58px;

            height: 58px;

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 16px;

            background: #FFF7E6;

            font-size: 30px;

        }

        .dominant-content {

            flex: 1;

        }

        .dominant-small {

            color: #98A2B3;

            font-size: 11px;

            font-weight: 700;

            letter-spacing: .8px;

        }

        .dominant-title {

            color: #01467D;

            font-size: 24px;

            font-weight: 700;

            margin: 2px 0;

        }

        .dominant-description {

            color: #667085;

            font-size: 13px;

        }

        .dominant-badge {

            padding: 9px 14px;

            border-radius: 999px;

            background: #EAF3FA;

            color: #01467D;

            font-size: 16px;

            font-weight: 700;

        }


        /* ==================================================
           BUTTON
        ================================================== */

        .stButton > button {

            width: 100%;

            border-radius: 12px;

            height: 48px;

            background: #01467D;

            color: white;

            font-weight: 600;

            border: none;

            transition: all .2s ease;

        }

        .stButton > button:hover {

            background: #0066B3;

            color: white;

            transform: translateY(-2px);

            box-shadow:
                0 7px 18px rgba(1, 70, 125, .18);

        }


        /* ==================================================
           TEXT AREA
        ================================================== */

        textarea {

            border-radius: 12px !important;

        }


        /* ==================================================
           ANIMATION
        ================================================== */

        @keyframes fadeUp {

            from {

                opacity: 0;

                transform:
                    translateY(12px);

            }

            to {

                opacity: 1;

                transform:
                    translateY(0);

            }

        }


        @keyframes resultEnter {

            from {

                opacity: 0;

                transform:
                    translateY(18px)
                    scale(.985);

            }

            to {

                opacity: 1;

                transform:
                    translateY(0)
                    scale(1);

            }

        }


        @keyframes emojiBounce {

            0%, 100% {

                transform:
                    translateY(0)
                    rotate(0deg);

            }

            50% {

                transform:
                    translateY(-5px)
                    rotate(-3deg);

            }

        }


        @keyframes progressGrow {

            from {

                transform:
                    scaleX(0);

            }

            to {

                transform:
                    scaleX(1);

            }

        }


        /* ==================================================
           MOBILE
        ================================================== */

        @media (max-width: 768px) {

            .st-key-navbar {

                width:
                    calc(100% - 30px) !important;

                top: 10px !important;

            }

            .block-container {

                padding-top:
                    100px !important;

            }

            .algorithm-info {

                flex-direction: column;

            }

            .result-hero {

                align-items:
                    flex-start;

            }

            .result-hero-title {

                font-size: 23px;

            }

            .dominant-card {

                align-items:
                    flex-start;

            }

            .dominant-badge {

                display: none;

            }

        }

        /* ==================================================
   DATASET PAGE
================================================== */

.dataset-title {
    font-size: 34px;
    font-weight: 700;
    color: #01467D;
    margin-bottom: 4px;

    animation: fadeUp .45s ease both;
}

.dataset-subtitle {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 26px;

    animation: fadeUp .55s ease both;
}


/* ==================================================
   PROCESS CARD
================================================== */

.process-card {
    position: relative;

    background: rgba(255,255,255,.95);

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 18px 22px;

    margin-top: 14px;
    margin-bottom: 14px;

    box-shadow:
        0 6px 18px rgba(15,23,42,.05);

    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease;

    animation:
        fadeUp .45s ease both;
}


/* efek hover */

.process-card:hover {
    transform: translateY(-3px);

    border-color: #C8DDED;

    box-shadow:
        0 12px 28px rgba(1,70,125,.09);
}


/* ==================================================
   NOMOR STEP
================================================== */

.process-number {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #01467D,
            #0066B3
        );

    color: white;

    font-size: 13px;
    font-weight: 700;

    margin-right: 9px;

    box-shadow:
        0 5px 12px rgba(1,70,125,.20);

    vertical-align: middle;
}


/* ==================================================
   TEXT PROCESS
================================================== */

.process-card b {
    color: #01467D;

    font-size: 16px;

    font-weight: 600;
}

.process-card br + * {
    color: #64748B;
}


/* ==================================================
   FILE UPLOADER
================================================== */

[data-testid="stFileUploader"] {

    background: white;

    border-radius: 18px;

    padding: 8px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 7px 20px rgba(15,23,42,.05);

    transition:
        border-color .25s ease,
        box-shadow .25s ease;
}


[data-testid="stFileUploader"]:hover {

    border-color: #9EC5E2;

    box-shadow:
        0 10px 25px rgba(1,70,125,.08);
}


/* ==================================================
   INFO BOX
================================================== */

.stAlert {

    border-radius: 16px !important;

    border: 1px solid #D8E7F5 !important;

    box-shadow:
        0 5px 15px rgba(15,23,42,.04);

    animation:
        fadeUp .45s ease both;
}


/* ==================================================
   DATAFRAME
================================================== */

[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 7px 20px rgba(15,23,42,.05);
}


/* ==================================================
   SUCCESS MESSAGE
================================================== */

[data-testid="stAlert"] {

    border-radius: 14px;
}


/* ==================================================
   BUTTON PREPROCESSING
================================================== */

.stButton > button {

    border-radius: 13px !important;

    min-height: 46px;

    font-family: 'Poppins', sans-serif !important;

    font-weight: 600 !important;

    transition:
        all .25s ease !important;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(1,70,125,.18);
}


/* ==================================================
   ANIMATION
================================================== */

@keyframes fadeUp {

    from {
        opacity: 0;

        transform:
            translateY(12px);
    }

    to {
        opacity: 1;

        transform:
            translateY(0);
    }
}

        </style>
        """,
        unsafe_allow_html=True
    )
