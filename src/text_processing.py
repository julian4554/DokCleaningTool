import re
def ersetze_umlaute(text):
    """
        Ersetzt Umlaute in einem Text.
        Args:
            text (str): Der Text, in dem Umlaute ersetzt werden sollen.
        Returns:
            str: Der Text mit ersetzen Umlauten.
        """
    umlaute = {
        'ae': 'ä',
        'oe': 'ö',
        'ue': 'ü',
        'Ae': 'Ä',
        'Oe': 'Ö',
        'Ue': 'Ü',
        'sz': 'ß'
    }
    for ersatz, umlaut in umlaute.items():
        text = text.replace(ersatz, umlaut)
    return text


# Funktion, um Leerzeichen vor Großbuchstaben einzufügen
def add_space_before_capital_letters(text):
    """
    Fügt Leerzeichen vor Großbuchstaben in einem Text ein.
    Args:
        text (str): Der Text, in dem Leerzeichen vor Großbuchstaben eingefügt werden sollen.
    Returns:
        str: Der Text mit eingefügten Leerzeichen vor Großbuchstaben.
    """
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)


# Funktion, um "Freitext" oder "txt" zu löschen
def loesche_txt(text):
    """
    Löscht "Freitext" oder "txt" aus einem Text.
    Args:
        text (str): Der Text, aus dem "Freitext" oder "txt" gelöscht werden soll.
    Returns:
        str: Der Text ohne "Freitext" oder "txt".
    """
    text = re.sub(r'\bTXT\b|\btxt\b', '', text, flags=re.IGNORECASE)
    return text


# Funktion, um "gepl" zu "geplant" auszuschreiben
def ersetze_gepl(text):
    """
       Ersetzt "gepl" durch "geplant" in einem Text.
       Args:
           text (str): Der Text, in dem "gepl" ersetzt werden soll.
       Returns:
           str: Der Text mit ersetzen "gepl".
       """
    return text.replace('gepl', 'geplant')


# Zentrale Funktion, die alle spezifischen Transformationen durchführt
def anpassen_text(text):
    """
    Führt alle spezifischen Textanpassungen durch.
    Args:
        text (str): Der Text, der angepasst werden soll.
    Returns:
        str: Der angepasste Text.
    """
    text = str(text)
    text = ersetze_umlaute(text)
    text = add_space_before_capital_letters(text)
    text = loesche_txt(text)
    text = ersetze_gepl(text)
    return text
