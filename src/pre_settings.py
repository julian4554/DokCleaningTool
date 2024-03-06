# pre_settings.py

# Voreingestellte Keywords, die auf die Daten angewendet werden sollen
KeyNichtAnalysieren = [
    "Procedere", "Fragestellung", "extern", "empfehlung", "empfehlungen", "prozedere"
]

KeyLöschen = [
    "historie", "datum", "kommentar", "Mitarbeiter", "histologie", "gewuenschte",
    "kostenuebernahme", "status", "versicherung"
]


def apply_pre_settings(df, column='TitelDB'):
    """
       Wendet vordefinierte Einstellungen auf das DataFrame an.
       Args:
           df (DataFrame): Das DataFrame, auf das die Einstellungen angewendet werden sollen.
           column (str, optional): Die Spalte, auf die die Einstellungen angewendet werden sollen. Default ist 'TitelDB'.
       Returns:
           DataFrame: Das bearbeitete DataFrame.
       """
    # Markieren von Zeilen mit Keywords für 'Nicht Analysieren'
    for keyword in KeyNichtAnalysieren:
        df.loc[df[column].str.lower().str.contains(keyword.lower()), 'Operation'] = 'Nicht Analysieren'

    # Löschen von Zeilen mit Keywords für 'Löschen'
    for keyword in KeyLöschen:
        df.loc[df[column].str.lower().str.contains(keyword.lower()), 'Operation'] = 'Löschen'

    return df
