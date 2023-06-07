# This file contains the necessary functions check accepted/rejected label for an amendment

# Get the label of amendment (accepted or rejected)
# This function is called in am2json.py by extracting first the html with the
# get_final_dossier_html and then calling this function on the text and final_dossier
import re
import string


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

