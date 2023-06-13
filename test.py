import sys, json
import argparse
import am2json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract amemdments.')
    parser.add_argument("dir", help="Directory containing the doc(x) files")
    parser.add_argument("legislature", help="Legislature number", type=int, default=9)
    parser.add_argument("-n", "--nb_of_documents", help="Number of document to proceed", type=int, required=False)
    args = parser.parse_args()
    data = am2json.extract_amendments_from_dir(args.dir, args.legislature, args.nb_of_documents)
    for dossier, articles in data.items():
        for name, a in articles.items():
            if len(a) > 1:
                print(f"{len(a)} amendments in conflict for {dossier} {name}")
    with open("dataset.json", "w") as f:
        json.dump(data, f, indent=2, separators=(',', ':'))