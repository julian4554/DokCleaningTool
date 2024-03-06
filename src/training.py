# training.py
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def load_and_prepare_data(folder_name):
    """
     Lädt Daten aus den Excel-Dateien im angegebenen Ordner und bereitet sie für das Training vor.
     Args:
         folder_name (str): Der Pfad zum Ordner mit den Excel-Dateien.
     Returns:
         tuple: Ein Tupel bestehend aus zwei Listen, all_X und all_y.
                all_X enthält alle Textdaten aus den Excel-Dateien.
                all_y enthält alle zugehörigen Labels.
     """
    all_X = []
    all_y = []

    for filename in os.listdir(folder_name):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_name, filename)
            df = pd.read_excel(file_path)
            df.fillna('', inplace=True)
            # Vor der Verknüpfung sicherstellen, dass alle Werte als Strings formatiert sind
            df['TitelDB'] = df['TitelDB'].astype(str)
            df['Beispiel'] = df['Beispiel'].astype(str)
            X = df['TitelDB'] + ' ' + df['Beispiel']
            y = df['Operation']

            all_X.extend(X)
            all_y.extend(y)

    return all_X, all_y


def train_model(all_X, all_y):
    """
       Trainiert ein Klassifikationsmodell auf den bereitgestellten Daten.
       Args:
           all_X (list): Eine Liste von Textdaten.
           all_y (list): Eine Liste von zugehörigen Labels.
       Returns:
           tuple: Ein Tupel bestehend aus dem trainierten Modell und dem Vektorizer.
                  Das trainierte Modell kann verwendet werden, um Vorhersagen zu treffen,
                  und der Vektorizer wurde auf die Trainingsdaten angepasst und kann
                  verwendet werden, um neue Textdaten zu transformieren.
       """
    vectorizer = CountVectorizer()
    model = MultinomialNB()
    X_all_vec = vectorizer.fit_transform(all_X)
    model.fit(X_all_vec, all_y)
    return model, vectorizer
