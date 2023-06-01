import requests
from bs4 import BeautifulSoup
from am2json.am2json import get_html, get_dossier_id


def get_final_dossier(dossier_id, download=False, debug=False):
    dossier_id_field = dossier_id.replace("PE", "")
    # First we create the URL GET request here
    url = 'https://www.europarl.europa.eu/committees/en/documents/search?committeeMnemoCode=&textualSearchMode=TITLE&textualSearch=&documentTypeCode=&reporterPersId=&procedureYear=&procedureNum=&procedureCodeType=&peNumber={dossier_id_field}&sessionDocumentDocTypePrefix=&sessionDocumentNumber=&sessionDocumentYear=&documentDateFrom=&documentDateTo=&meetingDateFrom=&meetingDateTo=&performSearch=true&term=9&page=0'.format(
        dossier_id_field=dossier_id_field)

    response = requests.get(url)

    # We take the HTML
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    result_divs = soup.find_all('div', class_='erpl_search-results-list-expandable-block')

    # Store docx link of final document here
    doc_link = False
    # Result should be 2 links, one for the draft and one for the final.
    # We take the one that's final (doesn't have DRAFT in title)
    if len(result_divs) == 2:
        try:
            for result_div in result_divs:
                # Get the title
                title = result_div.find('span', class_='t-item').text

                if "DRAFT" in title:
                    pass
                else:
                    # Get the document
                    doc_link = result_div.find('a', class_='erpl_document-subtitle-doc')['href']
                    if debug:
                        print(f"Got URL for dossier {dossier_id} with download link: {doc_link}")
                    doc_link = doc_link
                    break
        except:
            pass
    elif debug:
        print(f"Not exactly two files found for dossier {dossier_id}, but {len(result_divs)} files instead.")
    if download and doc_link:
        response = requests.get(doc_link)
        with open(f"./final_dossiers/{dossier_id}" + ".docx", 'wb') as file:
            file.write(response.content)
            if debug:
                print(f"Downloaded file {doc_link} successfully!")

    return doc_link


# directory has to be a Pathlib directory, gets all final dossiers based on
# a directory that contains the amendment documents.
def get_final_dossiers(directory, download=False, debug=False):
    doc_files = list(directory.rglob("*_EN.docx"))
    final_dossiers = []

    for doc_file in doc_files:
        soup = get_html(doc_file)
        dossier_id = get_dossier_id(soup)
        final_dossier = get_final_dossier(dossier_id, download=download, debug=debug)
        final_dossiers.append(final_dossier)
    return final_dossiers




def get_amendment_accepted(amend_text, dossier_id):
    pass

