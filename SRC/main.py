import tempfile
import logging
from src.data_loader import save_processed_data, TRAINING_DATA_DIR
from src.training import train_model, load_and_prepare_data, evaluate_model
from src.predict import predict_new_data
from GUI.main_gui import AnalyzerGUI


main_gui = AnalyzerGUI()
def main(file_path):
    """
    Main function to process new data, make predictions, apply pre-settings, and save the processed data.

    Args:
        file_path (str): The path to the new data file.
        main_gui (AnalyzerGUI): The instance of the AnalyzerGUI.
    Returns:
        str: The path to the processed data file.
    """
    try:
        # Daten vorbereiten und trainieren
        main_gui.progress_callback(40)
        logging.info("Loading and preparing training data.")
        all_X, all_y = load_and_prepare_data(TRAINING_DATA_DIR)
        model, vectorizer = train_model(all_X, all_y)
        evaluate_model(model, vectorizer, all_X, all_y)
        logging.info("Model training and evaluation complete. Ready to make predictions.")

        # Vorhersagen für neue Daten machen
        logging.info("Making predictions on new data.")

        df_predictions = predict_new_data(file_path, model, vectorizer)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', mode='w', encoding='utf-8', newline='',
                                         dir=TRAINING_DATA_DIR) as tmpfile:
            output_path = tmpfile.name
            logging.info(f"Saving processed data to {output_path}.")

            save_processed_data(df_predictions, output_path)

        return output_path

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        main(input_file)
    else:
        logging.error("No input file path provided.")
