import sys
import json


def get_instruction(group):
    return f"As member of the european parliament for the political group {group} I amend the submitted article text according to my values"


def print_json(a, group):
    print(json.dumps({'instruction': get_instruction(group), 'input': ' '.join(a['text_original']), 'output': ' '.join(a['text_amended'])}))


if __name__ == '__main__':
    file_path = sys.argv[1]
    if file_path.endswith('.json'):
        data = json.load(open(file_path))
        for dossier, articles in data.items():
            for article, edits in articles.items():
                for a in edits:
                    for author in a.get('authors', []):
                        group = author['group']
                        print_json(a, group)

    elif file_path.endswith('.jsonl'):
        with open(file_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                a = json.loads(line.rstrip())[0]
                if len(a['text_original']) == 0:
                    continue
                for author in a['authors']:
                    group = author['group']
                    print_json(a, group)
