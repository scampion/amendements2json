import sys, json
import argparse
from ep_amendment_extract import extract_amendments, extract_amendments_from_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract amemdments.')
    parser.add_argument("input", help="Directory containing the doc(x) files or a single doc(x) file")
    parser.add_argument("legislature", help="Legislature number", type=int, default=9)
    parser.add_argument("-n", "--nb_of_documents", help="Number of document to proceed", type=int, required=False)
    args = parser.parse_args()
    # test if args.input is a file or a directory
    if args.input.endswith(".docx") or args.input.endswith(".doc"):
        data = extract_amendments(args.input)
        print(json.dumps(list(data), indent=2))
    else:
        data = extract_amendments_from_dir(args.dir, args.legislature, args.nb_of_documents)
        for dossier, articles in data.items():
            for name, a in articles.items():
                if len(a) > 1:
                    print(f"{len(a)} amendments in conflict for {dossier} {name}")

