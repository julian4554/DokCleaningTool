import os
import shutil
import pandas as pd

# Basisverzeichnis für Daten
BASE_DIR = r"C:\Users\julia\PycharmProjects\Dedalus\data"

# Verzeichnisse für verschiedene Arten von Daten
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw")
RAW_USED_DATA_DIR = os.path.join(BASE_DIR, "rawUsed")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "processed")
TRAINING_DATA_DIR = os.path.join(BASE_DIR, "trainingData", "DatensätzeÜbung")


def move_file_to_raw_used(filename):
    """
    Verschiebt eine Datei vom 'raw'-Ordner in den 'rawUsed'-Ordner.
    """
    src_path = os.path.join(f'{filename}')
    dst_path = os.path.join(f'{RAW_USED_DATA_DIR}')
    shutil.move(src_path, dst_path)

#
def load_first_raw_data():
    """
    Lädt die erste Excel-Datei im 'raw'-Ordner und verschiebt sie nach 'rawUsed'.
    """
    filenames = os.listdir(RAW_DATA_DIR)
    if not filenames:
        raise FileNotFoundError("Keine Dateien im 'raw'-Ordner gefunden.")

    filename = filenames[0]  # Nehme die erste Datei
    file_path = os.path.join(RAW_DATA_DIR, filename)

    df = pd.read_excel(file_path).fillna('')

    return file_path  # Nur den Dateipfad zurückgeben



def save_processed_data(df, filename):
    """
    Speichert verarbeitete Daten im 'processed'-Ordner.
    """
    file_path = os.path.join(PROCESSED_DATA_DIR, filename)
    df.to_excel(file_path, index=False)


def save_training_data(df, filename):
    """
    Speichert Trainingsdaten im 'processed'-Ordner.
    """
    file_path = os.path.join(PROCESSED_DATA_DIR, filename)
    df.to_excel(file_path, index=False)



