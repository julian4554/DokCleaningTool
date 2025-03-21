import logging

# Voreingestellte Keywords, die auf die Daten angewendet werden sollen
KeyNichtAnalysieren = [
    "Procedere", "Fragestellung", "extern", "empfehlung", "empfehlungen", "prozedere", "prozedur", "prozeduren",
    "ICD10", "ICD11", "ICD12"
]

KeyLöschen = [
    "historie", "datum", "kommentar", "Mitarbeiter", "histologie", "gewuenschte",
    "kostenuebernahme", "status", "versicherung"
]


def apply_pre_settings(df, column='TitelDB'):
    """
    Applies predefined settings to the DataFrame.

    Args:
        df (DataFrame): The DataFrame to apply the settings to.
        column (str, optional): The column to apply the settings on. Default is 'TitelDB'.
    Returns:
        DataFrame: The modified DataFrame.
    """
    # Combine all keywords into one dictionary
    keywords = {
        'Nicht Analysieren': KeyNichtAnalysieren,
        'Löschen': KeyLöschen
    }

    for operation, keys in keywords.items():
        # Create a regex pattern for all keywords for each operation
        pattern = '|'.join([f'\\b{keyword.lower()}\\b' for keyword in keys])
        mask = df[column].str.lower().str.contains(pattern, na=False)
        df.loc[mask, 'Operation'] = operation
        logging.info(f"Applied {operation} to {mask.sum()} rows based on keywords: {keys}")

    return df
