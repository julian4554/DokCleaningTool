import json


def write_results_to_json(results, output_file):
    """
        Writes the analysis results to a JSON file.

        Args:
            results (dict): The analysis results to be written to the JSON file.
            output_file (str): The path to the output JSON file.
        """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
