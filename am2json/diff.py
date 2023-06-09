import difflib
import json


def diff(a, b):
    #a = [c + d for c, d in zip(a, a[1:])]
    #b = [c + d for c, d in zip(b, b[1:])]
    s = difflib.SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))

def zdiff(a, b):
    a = [c + d for c, d in zip(a, a[1:])]
    b = [c + d for c, d in zip(b, b[1:])]
    s = difflib.SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))


def get_replace(a, b):
    a = [c + d for c, d in zip(a, a[1:])]
    b = [c + d for c, d in zip(b, b[1:])]
    s = difflib.SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'replace' and ((i2 - i1) > 1 or (j2 - j1) > 1):
            yield tag, i1, i2, j1, j2


# def get_edits(a, b):
#     replacements = set(get_replace(a, b))
#     s = difflib.SequenceMatcher(None, a, b)
#     for tag, i1, i2, j1, j2 in s.get_opcodes():
#         if tag == 'insert' or tag == 'delete':
#             if replacements:
#                 in_replacement = False
#                 for r in replacements.copy():
#                     if r[1] == i1 and r[2] == i2 and r[3] == j1 and r[4] == j2:
#                         replacements.remove(r)
#                         yield tag, i1, i2, j1, j2
#             else:
#                 yield tag, i1, i2, j1, j2
#     for tag, i1, i2, j1, j2 in set(replacements):
#         yield tag, i1, i2, j1 - 2, j2 - 2

def get_edits(a, b):
    s = difflib.SequenceMatcher(None, a, b)
    edits = {(i1, i2, j1, j2): tag for tag, i1, i2, j1, j2 in s.get_opcodes() if tag in ['insert', 'delete', 'replace']}
    # for tag, i1, i2, j1, j2 in get_replace(a, b):
    #     if (i1, i2, j1, j2) not in list(edits.keys()):
    #         edits[(i1, i2, j1, j2)] = 'replace'

    for (i1, i2, j1, j2), tag in edits.items():
        yield tag, i1, i2, j1, j2


def get_edits_filtered(a, b):
    s = difflib.SequenceMatcher(None, a, b)
    current = None
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        print(tag, i1, i2, j1, j2)
        if tag in ['insert', 'delete', 'replace']:
            if current is None:
                current = (tag, i1, i2, j1, j2)
            elif current and tag != current[0] and i2 - i1 > 1:
                yield current
            elif current and tag != current[0] and i2 - i1 == 1:
                current[0] = 'replace'
                current[2] = i2
                current[4] = j2
    if current:
        yield current



def test():
    text_original = [
        "in",
        "carrying",
        "out",
        "its",
        "tasks",
        ",",
        "the",
        "agency",
        "shall",
        "maintain",
        "a",
        "close",
        "dialogue",
        "particularly",
        "with",
        "specialised",
        "bodies",
        ",",
        "whether",
        "public",
        "or",
        "private",
        ",",
        "public",
        "authorities",
        "and",
        "workers",
        "'",
        "and",
        "employers’",
        "organisations",
        ".",
        "the",
        "agency",
        ",",
        "without",
        "prejudice",
        "to",
        "its",
        "own",
        "aims",
        ",",
        "shall",
        "ensure",
        "cooperation",
        "with",
        "other",
        "european",
        "union",
        "agencies",
        "aimed",
        "at",
        "avoiding",
        "overlaps",
        "and",
        "promoting",
        "synergy",
        "and",
        "complementarity",
        "in",
        "their",
        "activities",
        ",",
        "in",
        "particular",
        "with",
        "the",
        "european",
        "foundation",
        "for",
        "the",
        "improvement",
        "of",
        "living",
        "and",
        "working",
        "conditions",
        ",",
        "the",
        "european",
        "centre",
        "for",
        "the",
        "development",
        "of",
        "vocational",
        "training",
        "and",
        ",",
        "where",
        "relevant",
        ",",
        "with",
        "other",
        "eu",
        "agencies",
        "."
    ]
    text_amended = [
        "in",
        "carrying",
        "out",
        "its",
        "tasks",
        "blabla",
        "blabla2",
        ",",
        "the",
        "agency",
        "shall",
        "maintain",
        "a",
        "close",
        "dialogue",
        "particularly",
        "with",
        "specialised",
        "public",
        "bodies",
        "or",
        "with",
        "the",
        "operating",
        "rules",
        "governing",
        "public",
        "law",
        ",",
        "public",
        "authorities",
        "and",
        "workers",
        "'",
        "and",
        "employers’",
        "organisations",
        ".",
        "the",
        "agency",
        ",",
        "without",
        "prejudice",
        "to",
        "its",
        "own",
        "aims",
        ",",
        "shall",
        "ensure",
        "cooperation",
        "with",
        "other",
        "european",
        "union",
        "agencies",
        "aimed",
        "at",
        "avoiding",
        "overlaps",
        "and",
        "promoting",
        "synergy",
        "and",
        "complementarity",
        "in",
        "their",
        "activities",
        ",",
        "in",
        "particular",
        "with",
        "the",
        "european",
        "foundation",
        "for",
        "the",
        "improvement",
        "of",
        "living",
        "and",
        "working",
        "conditions",
        ",",
        "the",
        "european",
        "centre",
        "for",
        "the",
        "development",
        "of",
        "vocational",
        "training",
        "and",
        ",",
        "where",
        "relevant",
        ",",
        # "with",
        # "other",
        "eu",
        "agencies",
        "."
    ]

    edit_type = "replace"
    edit_indices = {
        "i1": 16,
        "i2": 22,
        "j1": 16,
        "j2": 26
    }
    for tag, i1, i2, j1, j2 in get_edits(text_original, text_amended):
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, text_original[i1:i2], text_amended[j1:j2]))
    import IPython; IPython.embed()


if __name__ == '__main__':
    file_path = "/Users/scampion/src/WoW/data/canonical/war-of-words-2-ep8-chronological.txt"
    with open(file_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            a = json.loads(line.rstrip())[0]
            print(i, a['edit_type'], a['edit_indices'])
            found = False
            for j, (tag, i1, i2, j1, j2) in enumerate(get_edits_filtered(a['text_original'], a['text_amended'])):
                print('\t', j, tag, i1, i2, j1, j2)
                if a['edit_type'] == tag and a['edit_indices'] == {"i1": i1, "i2": i2, "j1": j1, "j2": j2}:
                    print('Founded', j)
                    found = True
                    break
            if not found and i not in [18]:
                print('Not found')
                print(set(get_edits_filtered(a['text_original'], a['text_amended'])))
                to = a['text_original']
                ta = a['text_amended']
                print("original ::::: " + ' '.join(a['text_original']))
                print("amended  ::::: " + ' '.join(a['text_amended']))
                import IPython; IPython.embed()
                break

            print('-----')
            if i > 20:
                break
