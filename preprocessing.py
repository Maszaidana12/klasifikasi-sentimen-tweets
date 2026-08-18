import re
import pandas as pd
import csv

from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory
)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from Sastrapy.WordTokenize.Tokenize import (
    tokenize
)

# =====================================================
# 1. CLEANING
# =====================================================

def cleaning(teks):

    if pd.isna(teks):
        return ""

    teks = str(teks).lower()

    # Hapus mention
    teks = re.sub(r'@\w+', '', teks)

    # Hapus hashtag
    teks = re.sub(r'#\w+', '', teks)

    # Hapus URL
    teks = re.sub(
        r'https?://\S+|www\.\S+',
        '',
        teks
    )

    # Hapus selain huruf
    teks = re.sub(
        r'[^a-z\s]',
        ' ',
        teks
    )

    # Rapikan spasi
    teks = re.sub(
        r'\s+',
        ' ',
        teks
    ).strip()

    return teks


# ==========================================
# TOKENIZING
# ==========================================


def tokenizing(teks):

    if pd.isna(teks):
        return teks

    return tokenize(teks)


# =====================================================
# NORMALISASI SLANG
# =====================================================

# =====================================================
# NORMALISASI SLANG
# =====================================================

def load_kamus_slang():

    kamus = {}

    file_kamus = [
        "data/kamusalay1.csv",
        "data/slangword_indonesia.csv"
    ]

    for nama_file in file_kamus:

        try:

            with open(
                nama_file,
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                for row in reader:

                    if len(row) >= 2:

                        kata_slang = (
                            row[0]
                            .strip()
                            .lower()
                        )

                        kata_normal = (
                            row[1]
                            .strip()
                            .lower()
                        )

                        if (
                            kata_slang
                            and kata_normal
                        ):

                            kamus[
                                kata_slang
                            ] = kata_normal

        except FileNotFoundError:

            print(
                f"Kamus tidak ditemukan: {nama_file}"
            )

    return kamus


kamus_slang = load_kamus_slang()


def normalisasi_slang(tokens):

    if tokens is None:
        return []

    hasil = []

    for word in tokens:

        word_normal = kamus_slang.get(
            word,
            word
        )

        hasil.append(word_normal)

    return hasil
# =====================================================
# 2. STOPWORD
# =====================================================

stop_words_lainnya = [

    'yang', 'dan', 'di', 'ke', 'dari',
    'akan', 'hal', 'lho', 'aja',
    'kalau', 'sih', 'si', 'lah',
    'ya', 'oleh', 'para', 'dengan',
    'tapi', 'lagi', 'untuk', 'mereka',
    'ini', 'itu', 'bisa', 'sangat',
    'dong', 'nya', 'nih', 'nah',
    'kok', 'pun', 'deh'

]

factory = StopWordRemoverFactory()

stop_words_sastrawi = (
    factory.get_stop_words()
)

stop_words = list(
    set(
        stop_words_sastrawi +
        stop_words_lainnya
    )
)


def remove_stopword(tokens):

    if not tokens:
        return []

    hasil = []

    for word in tokens:

        if word not in stop_words:
            hasil.append(word)

    return hasil


# =====================================================
# 3. STEMMING
# =====================================================

stemmer_factory = StemmerFactory()

stemmer = (
    stemmer_factory.create_stemmer()
)


def stemming(tokens):

    if not tokens:
        return []

    hasil = []
    for word in tokens:

        hasil.append(
            stemmer.stem(word)
        )

    return hasil

# =====================================================
# 4. PREPROCESSING UTAMA
# =====================================================

def preprocess(teks):

    teks = cleaning(teks)
    teks = tokenizing(teks)
    teks = normalisasi_slang(teks)
    teks = remove_stopword(teks)
    teks = stemming(teks)
    teks = " ".join(teks)
    return teks

if __name__ == "__main__":

    teks = "Pemerintah gk becus ngurus banjir!"

    hasil_cleaning = cleaning(teks)

    hasil_tokenizing = tokenizing(
        hasil_cleaning
    )

    hasil_normalisasi = normalisasi_slang(
        hasil_tokenizing
    )

    hasil_stopword = remove_stopword(hasil_normalisasi)
    hasil_stemming = stemming(hasil_stopword)



    print("Input        :", teks)
    print("Cleaning     :", hasil_cleaning)
    print("Tokenizing   :", hasil_tokenizing)
    print("Normalisasi  :", hasil_normalisasi)
    print("Stopword     :", hasil_stopword)
    print("stemming     :", hasil_stemming)
    print(
        "Preprocessing:",
        preprocess(teks)
    )

    print(
        "Jumlah kata dalam kamus:",
        len(kamus_slang)
    )


if __name__ == "__main__":

    print(
        "Jumlah kata dalam kamus:",
        len(kamus_slang)
    )

    teks = "Pemerintah gk becus ngurus banjir!"

    print(
        "Input:",
        teks
    )

    print(
        "Preprocessing:",
        preprocess(teks)
    )
    