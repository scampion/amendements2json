import pathlib

import requests
from bs4 import BeautifulSoup


# Based on dossier ID, extract files from base URL (has to be 2 files, 1 draft, 1 final) through GET request
def get_final_dossier_link(dossier_id, download=False, debug=False):
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






