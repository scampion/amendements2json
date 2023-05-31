import difflib
import json
import sys
import logging
from bs4 import BeautifulSoup
import re

from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

import am2json.meps as meps

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

mep_info = meps.get_mep_data()


def clean(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        for r in re.findall(r'\{(.*?)\}$', text):
            text = r
            break
        for r in re.findall(r'\((.*?)\)$', text):
            text = r
            break
        return text

    return wrapper


# def get_html(doc_file):
#     doc = Document(doc_file)
#     text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
#     soup = BeautifulSoup(text_content, 'html.parser')
#     return soup


def get_html(file):
    def iter_block_items(parent):
        """
        Generate a reference to each paragraph and table child within *parent*,
        in document order. Each returned value is an instance of either Table or
        Paragraph. *parent* would most commonly be a reference to a main
        Document object, but also works for a _Cell object, which itself can
        contain paragraphs and tables.
        """
        if isinstance(parent, _Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        elif isinstance(parent, _Row):
            parent_elm = parent._tr
        else:
            raise ValueError("something's not right")
        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    document = Document(file)

    html_string = ""
    for block in iter_block_items(document):
        # print(block.text if isinstance(block, Paragraph) else '<table>')
        if isinstance(block, Paragraph):
            if block.text:
                html_string += block.text + "<br>"
        elif isinstance(block, Table):
            html_string += "<table>"
            for row in block.rows:
                if any(cell.text.strip() for cell in row.cells):  # Check if any cell in the row is non-empty
                    html_string += "<tr>"
                    row_data = []
                    for cell in row.cells:
                        cell_text = " ".join([paragraph.text for paragraph in cell.paragraphs])
                        html_string += f"<td>{cell_text}</td>"
                    html_string += "</tr>"

            html_string += "</table>"

    soup = BeautifulSoup(html_string, "html.parser")
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
    return soup.find("date").text


def get_article_type(soup):
    if soup.find("article"):
        article_type = soup.find("article").text.strip()
        return article_type.split(' ')[0].lower()

def get_titretype(soup):
    if soup.find('titretype'):
        return soup.find('titretype').text.strip().split()[-1].lower()


def get_legal_act(soup):
    # Find the <docref> tag cause the legal type is after the <br> right next to it.

    try:
        docref_tag = soup.find('docref')

        br_tag = docref_tag.find_next('br')

        leg_type = br_tag.next_sibling.string.strip()
    except:
        leg_type = "NA"

    # Check if document is a resolution
    if "Non" in leg_type:
        return "resolution"
    elif soup.find(text="Proposal for a directive"):
        return "directive"

    elif soup.find(text="Proposal for a regulation"):
        return "regulation"

    elif soup.find(text="Proposal for a decision"):
        return "decision"
    else:
        return "None"






def get_metadata(soup):
    return {'committee': get_committee(soup),
            'dossier_ref': get_dossier_ref(soup),
            'date': get_date(soup),
            'rapporteur': soup.find("rapporteur").text.strip(),
            'source': get_source(soup),
            'article_type': get_article_type(soup),
            'dossier_title': soup.find("titre").text.strip(),
            'dossier_type': get_titretype(soup),
            'legal_act': get_legal_act(soup),
            'justification': None
            }


def get_amd(amend):
    table = amend.find("table")
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
    def get_mep_info(name):
        global mep_info
        for mep_id, mep_data in mep_info.items():
            if mep_data.get('name').lower() == name.lower():
                return mep_id, mep_data

    for author in [author.strip() for author in amend.find("members").text.split(",")]:
        mep_id, mep_data = get_mep_info(author)
        if mep_data:
            yield {
                'id': int(mep_id),
                'name': mep_data.get('name'),
                'gender': mep_data.get('gender'),
                'nationality': mep_data.get('nationality'),
                'group': mep_data.get('group-ep9'),
                'rapporteur': False
            }


def get_amend_num(amend):
    if amend.find("numam"):
        return amend.find("numam").text.strip()


def get_amendments(soup):
    md = get_metadata(soup)
    for amend in soup.find_all("amend"):
        md['authors'] = list(get_authors(amend))
        md['amendment_num'] = get_amend_num(amend)
        md['text_original'], md['text_amended'], md['edit_type'], md['edit_indices'] = get_amd(amend)
        yield md


def extract_amendments(file):
    soup = get_html(file)
    assert soup.find("typeam") and soup.find("typeam").text.strip() == "AMENDMENTS", "Not an amendment file"
    md = get_metadata(soup)
    for i, a in enumerate(get_amendments(soup)):
        yield md | a


if __name__ == '__main__':
    soup = get_html(sys.argv[1])
    with open(sys.argv[1] + ".json", "w") as f:
        json.dump(soup.prettify(), f, indent=2)
    for i, r in enumerate(extract_amendments(sys.argv[1])):
        with open(sys.argv[1] + f"_{i}.json", 'w') as f:
            json.dump(r, f, indent=2, separators=(',', ':'))
        print(json.dumps(r, indent=2, separators=(',', ':')))
        print("-" * 80)
