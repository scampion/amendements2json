import sys
import json

if __name__ == '__main__':
    file_path = sys.argv[1]
    with open(file_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            a = json.loads(line.rstrip())[0]
            if len(a['text_original']) == 0:
                continue
            for author in a['authors']:
                group = author['group']
                instruction = f"As member of the european parliament for the political group {group}, I propose to amend the text submitted as follows:"
                print(json.dumps({'instruction': instruction,
                                    'input': ' '.join(a['text_original']),
                                    'output': ' '.join(a['text_amended'])}))
