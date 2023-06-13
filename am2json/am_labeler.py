# This file contains the necessary functions check accepted/rejected label for an amendment

# Get the label of amendment (accepted or rejected)
# This function is called in am2json.py by extracting first the html with the
# get_final_dossier_html and then calling this function on the text and final_dossier
import re
import string
from io import BytesIO

import requests

from amendements2json.am2json import get_html
from amendements2json.am2json.am2json import extract_final_amendments, get_dossier_id


def remove_enumeration_pattern(text):
    """
    Remove the enumeration pattern from the given text.
    """
    return re.sub(r'^[-\w]+\.\s*|^-\s*|–\s*|—\s*', '', text)


def preprocess_text(am):
    # Remove all whitespace space, tabs etc)
    am = re.sub(r'\s+', '', am)
    # Remove punctuation
    am = am.translate(str.maketrans('', '', string.punctuation))
    # Lower the text
    am = am.lower()
    return am


def get_label_am(am_text, final_amendments):
    if isinstance(am_text, list):
        am_text = " ".join(am_text)
    am_text = remove_enumeration_pattern(am_text)
    am_text = preprocess_text(am_text)
    final_amendments = [preprocess_text(text) for text in final_amendments]
    if am_text in final_amendments:
        return True
    else:
        return False


# Parameter local defines whether to get the file from local directory
# Otherwise get it online
# Based on dossier ID, look for link or local file to get final amendments docx, and then apply extract_final_amendments.
def get_final_dossier_am(dossier_id, local=False):

    if local:
        dossier_file = f"./final_dossiers/{dossier_id}.docx"
        amendments = extract_final_amendments(dossier_file)
        return amendments
    else:
        url_link = get_final_dossier_link(dossier_id)
        if url_link:
            response = requests.get(url_link)
            file_in_mem = BytesIO(response.content)
            amendments = extract_final_amendments(file_in_mem)
            return amendments
        else:
            return []

# directory has to be a Pathlib directory, gets all final dossiers based on
# a directory that contains the amendment documents.

def get_final_dossiers(directory, download=False, debug=False):
    doc_files = list(directory.rglob("*_EN.docx"))
    final_dossiers = []

    for doc_file in doc_files:
        soup = get_html(doc_file)
        dossier_id = get_dossier_id(soup)
        final_dossier = get_final_dossier_link(dossier_id, download=download, debug=debug)
        final_dossiers.append(final_dossier)
    return final_dossiers
