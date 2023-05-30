import difflib
import json
import sys
import logging
from bs4 import BeautifulSoup
import re

from docx import Document

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def clean(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        for r in re.findall(r'\{(.*?)\}', text):
            text = r
            break
        for r in re.findall(r'\((.*?)\)', text):
            text = r
            break
        return text
    return wrapper

def get_html(doc_file):
    doc = Document(doc_file)
    text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    soup = BeautifulSoup(text_content, 'html.parser')
    return soup


def get_parliament(soup):
    if soup.find("td"):
        return soup.find("td").text.strip()
    else:
        log.warning("No parliament found")


@clean
def get_committee(soup):
    return soup.find("commission").text.strip().replace("Committee on ", "")


@clean
def get_dossier_ref(soup):
    if soup.find("refproc"):
        return soup.find("refproc").text.strip()
    elif soup.find("docrefpe"):
        return soup.find("docrefpe").text.strip()



@clean
def get_source(soup):
    if soup.find("docref"):
        return soup.find("docref").text.strip()
    elif soup.find("docrefpe"):
        return soup.find("docrefpe").text.strip()


@clean
def get_date(soup):
    return  soup.find("date").text


def get_metadata(soup):
    return {'committee': get_committee(soup),
            'dossier_ref': get_dossier_ref(soup),
            'date': get_date(soup),
            'rapporteur': soup.find("rapporteur").text.strip(),
            'source': get_source(soup),
            'dossier_title': soup.find("titre").text.strip()
            }


def get_amd(amend):
    table = amend.find("table")
    if not table:
        return None, None, None, None
    draft_opinion = table.find_all("tr")[1].find_all("td")[0].text.strip()
    amendment = table.find_all("tr")[1].find_all("td")[1].text.strip()

    # We get here the edit_indices and edit type using difflib
    diff = difflib.ndiff(draft_opinion.split(), amendment.split())
    edit_type = None
    diff_indices = {'i1': 0, 'i2': 0, 'j1': 0, 'j2': 0}

    for i, line in enumerate(diff):
        if line.startswith('-'):
            edit_type = 'delete'
            diff_indices['i1'] = i
            diff_indices['i2'] = i + 1
            diff_indices['j1'] = i
            diff_indices['j2'] = i
            break
        elif line.startswith('+'):
            edit_type = 'insert'
            diff_indices['i1'] = i
            diff_indices['i2'] = i
            diff_indices['j1'] = i
            diff_indices['j2'] = i + 1
            break
        elif line.startswith('?'):
            edit_type = 'replace'
            diff_indices['i1'] = i
            diff_indices['i2'] = i + 1
            diff_indices['j1'] = i
            diff_indices['j2'] = i + 1
            break
    return draft_opinion, amendment, edit_type, diff_indices


def get_authors(amend):
    mep_info = json.load(open("mep_info.json", 'r'))
    author_names = [author.text.strip() for author in amend.find_all("members")]
    authors = []
    for author_name in author_names:
        author_data = None
        for mep_id, mep_data in mep_info.items():
            if mep_data.get('name').lower() == author_name.lower():
                author_data = mep_data
                break
        if author_data:
            author = {
                'id': int(mep_id),
                'name': author_data.get('name'),
                'gender': author_data.get('gender'),
                'nationality': author_data.get('nationality'),
                'group': author_data.get('group-ep9'),
                'rapporteur': False
            }
            authors.append(author)
    return authors


def get_amendments(soup):
    md = get_metadata(soup)
    for amend in soup.find_all("amend"):
        md['authors'] = get_authors(amend)
        md['amendment_num'] = amend.find("num").text.strip() if amend.find("num") else None
        md['draft_opinion'], md['amendment'], md['edit_type'], md['diff_indices'] = get_amd(amend)
        yield md


if __name__ == '__main__':
    soup = get_html(sys.argv[1])
    assert soup.find("typeam") and soup.find("typeam").text.strip() == "AMENDMENTS", "Not an amendment file"
    with open(sys.argv[1]+".html", 'w') as f:
        f.write(soup.prettify())
    md = get_metadata(soup)

    for a in get_amendments(soup):
       r = md | a
       print(json.dumps(r, indent=4, separators=(',', ':')))
       print("#" * 80)
