from am2json.am2json import extract_amendments
from am2json.am2json import get_html
from am2json.am2json import get_final_dossier_html, get_label_am
import pathlib
import json
directory = pathlib.Path("./data")

# Download the final dossiers
# final_dossiers = get_final_dossiers(directory, download=True, debug=True)

# Test to see if we can find extracted amendment back in final dossier

amendments_example = extract_amendments("./data/AFET_AM(2020)648337_EN.docx")
amendments = list(amendments_example)


def run_test(amendments, idx):

    dossier_id = amendments[idx]["dossier_id"]

    html_final = get_final_dossier_html(dossier_id)

    am_text = amendments[idx]["text_amended"]

    if isinstance(am_text, list):
        am_text = " ".join(am_text)

    if am_text.startswith("-") or am_text.startswith("–"):
        am_text = am_text[1:]

    print("------------------")
    print("------------------")
    #print(am_text)
    print("------------------")
    #print(html_final)
    print("------------------")
    print(get_label_am(am_text, html_final))
    print("------------------")
    print("------------------")


# Should return True
run_test(amendments, 0)
# Should return True
run_test(amendments, 2)
# Should return False
run_test(amendments, 3)


#run_test(amendments, 4)
