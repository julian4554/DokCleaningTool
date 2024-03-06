# main.py
from src.data_loader import load_first_raw_data, save_processed_data, move_file_to_raw_used, TRAINING_DATA_DIR
from src.training import train_model, load_and_prepare_data
from src.predict import predict_new_data
from src.pre_settings import apply_pre_settings



def main():


    try:
        # Laden der ersten Rohdaten und Verschieben in den entsprechenden Ordner
        file_path = load_first_raw_data()
        # Daten vorbereiten und trainieren
        all_X, all_y = load_and_prepare_data(TRAINING_DATA_DIR)  # Übergeben Sie den Dateipfad an load_and_prepare_data
        model, vectorizer = train_model(all_X, all_y)

        # Vorhersagen für neue Daten machen
        df_predictions = predict_new_data(file_path, model, vectorizer)

        # Anwenden der Voreinstellungen auf die Vorhersagen
        df_predictions = apply_pre_settings(df_predictions)

        # Speichern der verarbeiteten Daten
        output_path = r'C:\Users\julia\PycharmProjects\Dedalus\data\processed\Vorhersagen_Bearbeitet.xlsx'
        save_processed_data(df_predictions, output_path)

    finally:
        # Verschieben der Rohdatendatei in den Ordner 'rawUsed' nach Abschluss aller anderen Aktionen
        move_file_to_raw_used(file_path)

if __name__ == '__main__':
    main()
