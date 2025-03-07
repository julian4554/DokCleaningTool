OrbisKi is a Python-based tool designed to analyze and classify textual data, 
particularly suited for processing medical and clinical datasets. It automates data preprocessing, 
text adjustments, and classification using machine learning techniques, 
facilitating efficient and accurate data insights.

---------------------------------------------------------------------------------------------------------

Features

Data Preprocessing: Automated loading and cleaning of textual data from Excel files.

Text Adjustment: Custom text normalization including correction of common typographical errors and formatting inconsistencies.

Machine Learning Classification: Implements a Multinomial Naive Bayes model optimized with GridSearchCV to classify data accurately.

Data Export: Predicts and saves processed data into Excel files for further analysis or reporting.

---------------------------------------------------------------------------------------------------------
![image](https://github.com/user-attachments/assets/e28ccb4d-23fe-4cf2-a212-9d667cf0eba7)
---------------------------------------------------------------------------------------------------------

Structure

data_loader.py: Handles loading and saving of training and processed datasets.
text_processing.py: Contains methods for cleaning and adjusting text data.
training.py: Prepares data, trains, and evaluates machine learning models.
predict.py: Uses trained models to predict new data classifications.

---------------------------------------------------------------------------------------------------------

Dependencies

Python 3.x
pandas
sklearn
openpyxl

