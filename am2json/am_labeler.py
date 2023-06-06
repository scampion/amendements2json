# This file contains the necessary functions check accepted/rejected label for an amendment

# Get the label of amendment (accepted or rejected)
# This function is called in am2json.py by extracting first the html with the
# get_final_dossier_html and then calling this function on the text and final_dossier
import re


def get_label_am(am_text, final_dossier_soup):
    if isinstance(am_text, str):
        am_text = am_text.split()

    if am_text[0] in ["-", "–"]:
        am_text = am_text[1:]

    am_text = [text.lower() for text in am_text]

    final_dossier_soup = str(final_dossier_soup).lower()

    # Remove html tags
    clean_soup = re.sub('<[^<]+?>', '', final_dossier_soup)

    clean_soup = ''.join(clean_soup.split())
    am_text = ''.join(am_text)

    if am_text in clean_soup:
        return True
    else:
        return False

