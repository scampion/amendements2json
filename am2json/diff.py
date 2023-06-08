import difflib

def diff(a, b):
    current_edit = None
    for d in difflib.ndiff(a, b):
        print(d)
        if d[0] == ' ':
            if current_edit:
                yield current_edit
                current_edit = None
        elif d[0] == '-':
            if current_edit and current_edit['type'] == 'delete':
                current_edit['text'] += d[2:]
            else:
                if current_edit:
                    yield current_edit
                current_edit = {'type': 'delete', 'text': d[2:]}
        elif d[0] == '+':
            if current_edit and current_edit['type'] == 'insert':
                current_edit['text'] += d[2:]
            else:
                if current_edit:
                    yield current_edit
                current_edit = {'type': 'insert', 'text': d[2:]}
        elif d[0] == '?':
            if current_edit:
                yield current_edit
                current_edit = None
    if current_edit:
        yield current_edit