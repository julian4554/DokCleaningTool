import os
import pandas as pd
import logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_and_prepare_data(folder_name):
    """
    Loads data from the Excel files in the specified folder and prepares it for training.

    Args:
        folder_name (str): The path to the folder containing the Excel files.
    Returns:
        tuple: A tuple consisting of two lists, all_X and all_y.
               all_X contains all text data from the Excel files.
               all_y contains all corresponding labels.
    """
    all_X = []
    all_y = []

    for filename in os.listdir(folder_name):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_name, filename)
            try:
                df = pd.read_excel(file_path)
                logging.info(f"Successfully read {file_path}")
            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
                continue

            # Check if the necessary columns exist
            if 'TitelDB' in df.columns and 'Beispiel' in df.columns and 'Operation' in df.columns:
                # Ensure specific columns are of type string before filling NaN values
                df['TitelDB'] = df['TitelDB'].astype(str)
                df['Beispiel'] = df['Beispiel'].astype(str)

                # Fill NaN values appropriately
                for column in df.columns:
                    if df[column].dtype == 'object':
                        df[column] = df[column].fillna('')
                    elif df[column].dtype in ['int64', 'float64']:
                        df[column] = df[column].fillna(0)

                # Prepare data for training
                X = df['TitelDB'] + ' ' + df['Beispiel']
                y = df['Operation']

                all_X.extend(X)
                all_y.extend(y)
            else:
                logging.warning(f"Missing columns in {file_path}")
                continue

    return all_X, all_y


def train_model(all_X, all_y):
    """
    Trains a classification model on the provided data.

    Args:
        all_X (list): A list of text data.
        all_y (list): A list of corresponding labels.
    Returns:
        tuple: A tuple consisting of the trained model and the vectorizer.
               The trained model can be used to make predictions,
               and the vectorizer has been fitted to the training data and can
               be used to transform new text data.
    """
    vectorizer = CountVectorizer()
    X_all_vec = vectorizer.fit_transform(all_X)

    model = MultinomialNB()

    # Parameter tuning using GridSearchCV
    param_grid = {
        'alpha': [0.1, 0.5, 1.0]
    }
    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(X_all_vec, all_y)

    best_model = grid_search.best_estimator_

    logging.info("Model training complete. Best parameters: %s", grid_search.best_params_)

    return best_model, vectorizer


def evaluate_model(model, vectorizer, all_X, all_y):
    """
    Evaluates the trained model on a test set and logs the accuracy.

    Args:
        model: The trained model.
        vectorizer: The fitted vectorizer.
        all_X (list): A list of text data.
        all_y (list): A list of corresponding labels.
    """
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(all_X, all_y, test_size=0.2, random_state=42)

    # Transform the test data using the fitted vectorizer
    X_test_vec = vectorizer.transform(X_test)

    # Make predictions on the test data
    y_pred = model.predict(X_test_vec)

    # Calculate the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy: {accuracy * 100:.2f}%")



