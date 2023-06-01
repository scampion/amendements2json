import sys, json

import am2json


if __name__ == '__main__':
    with open(sys.argv[1] + ".html", 'w') as f:
        soup = am2json.get_html(sys.argv[1])
        f.write(soup.prettify())
    with open(sys.argv[1] + ".json", "w") as f:
        for amend in am2json.extract_amendments(sys.argv[1]):
            f.write(json.dumps(amend, ensure_ascii=False, sort_keys=True))
            f.write("\n")