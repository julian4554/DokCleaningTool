# predict.py
import pandas as pd
from text_processing import anpassen_text
from pre_settings import apply_pre_settings


def predict_new_data(new_data_path, model, vectorizer):
    """
       Macht Vorhersagen für neue Daten unter Verwendung des trainierten Modells und Vektorizers.
       Args:
           new_data_path (str): Der Pfad zur Datei mit den neuen Daten.
           model: das trainierte Klassifikationsmodell.
           vectorizer: Der trainierte Vektorizer.
       Returns:
           pandas. DataFrame: Ein DataFrame mit den vorhergesagten Labels für die neuen Daten.
       """
    # Neue Daten laden
    df_new_data = pd.read_excel(new_data_path)
    df_new_data.fillna('', inplace=True)

    df_new_data['TitelAnzeige'] = df_new_data['TitelAnzeige'].apply(anpassen_text)
    df_new_data = apply_pre_settings(df_new_data)

    # Daten vorbereiten
    X_new_data = df_new_data[['TitelDB', 'Beispiel']].astype(str)

    # Text vektorisieren
    X_new_data_vec = vectorizer.transform(X_new_data['TitelDB'] + ' ' + X_new_data['Beispiel'])

    # Vorhersagen für neue Daten machen
    predictions_new_data = model.predict(X_new_data_vec)

    # Füge die Vorhersagen der neuen Daten in die Spalte 'Operation' der neuen Tabelle ein
    df_new_data['Operation'] = predictions_new_data

    return df_new_data


