import io
import tempfile
import zipfile

import requests
import xml.etree.ElementTree as ET
import csv
import json
import os


def get_mep_gender():
    url = "https://www.tttp.eu/data/meps.csv"
    r = requests.get(url)
    if r.status_code == 200:
        csv_reader = csv.reader(r.content.decode('utf-8').splitlines(), delimiter=',')
        genders = {}
        for row in csv_reader:
            genders[row[0]] = row[6], row[2] + row[3]
        return genders


def get_mep_data_from_web():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    url = "https://www.europarl.europa.eu/meps/en/full-list/xml/"
    data = {}
    genders = get_mep_gender()
    for letter in alphabet:
        letter_url = url + letter
        r = requests.get(letter_url)
        if r.status_code != 200:
            continue
        content = r.content
        tree = ET.fromstring(content)
        if not tree:
            continue
        for mep in tree.findall('mep'):
            id = mep.find('id').text
            name = mep.find('fullName').text
            country = mep.find('country').text
            # group-ep8
            group = mep.find('politicalGroup').text
            print(id, name, country)
            try:
                gender, _ = genders.get(id, ("X", "Not found"))
                print(id, name, country, gender)
                data[id] = {"name": name, "nationality": country, "group-ep9": group, "gender": gender}
            except Exception as e:
                print("🌩️ Error " + str(e))
                continue

    outgoing = "https://www.europarl.europa.eu/meps/en/incoming-outgoing/outgoing/xml"
    r = requests.get(outgoing)
    content = r.content
    tree = ET.fromstring(content)
    for mep in tree.findall('mep'):
        id = mep.find('id').text
        name = mep.find('fullName').text
        country = mep.find('country').text
        # group-ep8
        group = mep.find('politicalGroup').text
        print("Outgoing", id, name, country)
        try:
            gender, _ = genders.get(id, ("X", "Not found"))
            print(id, name, country, gender)
            data[id] = {"name": name, "nationality": country, "group-ep9": group, "gender": gender}
        except Exception as e:
            print("🌩️ Error " + str(e))
            continue

    return data


def get_previous_mep_data():
    url = "https://zenodo.org/record/4709248/files/helpers.zip?download=1"
    r = requests.get(url)
    if r.status_code == 200:
        iob = io.BytesIO(r.content)
        with zipfile.ZipFile(iob, 'r') as zip_ref, tempfile.TemporaryDirectory() as tmpdir:
            zip_ref.extract('helpers/meps.json', tmpdir)
            with open(os.path.join(tmpdir, 'helpers/meps.json'), 'r') as f:
                return json.load(f)


def get_mep_data():
    user_dir = os.path.expanduser('~')
    data_dir = os.path.join(user_dir, '.amendements2json')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    data_file = os.path.join(data_dir, 'meps.json')
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = get_mep_data_from_web()
        for k, v in get_previous_mep_data().items():
            if k not in data.keys():
                data[k] = v
            else:
                data[k] = {**data[k], **v}
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
    return data


if __name__ == '__main__':
    data = get_mep_data()
    json.dumps(data, indent=2)
