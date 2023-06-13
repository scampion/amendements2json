from am2json.am2json import extract_amendments
from am2json.am2json import get_html
from am2json.am2json import get_final_dossier_am, get_label_am
from am2json.am_labeler import remove_enumeration_pattern
import pathlib
import json
directory = pathlib.Path("./data")

# Download the final dossiers
# final_dossiers = get_final_dossiers(directory, download=True, debug=True)

# Test to see if we can find extracted amendment back in final dossier

amendments_example = extract_amendments("./data/AFET_AM(2020)648337_EN.docx")
amendments_example2 = extract_amendments("./data/EMPL_AM(2023)740808_EN.docx")
amendments = list(amendments_example)
amendments_2 = list(amendments_example2)


def run_test(amendments, idx):

    dossier_id = amendments[idx]["dossier_id"]

    final_amendments = get_final_dossier_am(dossier_id)

    am_text = amendments[idx]["text_amended"]
    if isinstance(am_text, list):
        am_text = " ".join(am_text)
    text = remove_enumeration_pattern(am_text)


    print("------------------")
    print("------------------")
    print(text)
    print("------------------")
    print(final_amendments)
    print("------------------")
    print(get_label_am(am_text, final_amendments))
    print("------------------")
    print("------------------")


# Should return True
#run_test(amendments, 0)
# Should return True
#run_test(amendments, 2)
# Should return False
#run_test(amendments, 3)


# should return False
run_test(amendments_2, 0)
# should return False
run_test(amendments_2, 2)
# should return False
run_test(amendments_2, 4)
