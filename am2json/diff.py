import difflib
import json


def extract_opcodes(a_words, b_words):
    matcher = difflib.SequenceMatcher(None, a_words, b_words)
    opcodes = matcher.get_opcodes()
    merged_opcodes = []
    skip = False
    for i in range(len(opcodes)):
        if skip:
            skip = False
            continue
        opcode = opcodes[i]
        if 0 < i < len(opcodes) - 1 and opcode[0] == 'equal' and (opcode[2] - opcode[1]) == 1:
            prev_opcode = merged_opcodes.pop()
            next_opcode = opcodes[i + 1]
            merged_opcodes.append(('replace', prev_opcode[1], next_opcode[2], prev_opcode[3], next_opcode[4]))
            skip = True
        elif opcode[0] != 'equal':
            merged_opcodes.append(opcode)
    return merged_opcodes


if __name__ == '__main__':
    file_path = "../../data/canonical/war-of-words-2-ep8-chronological.txt"
    with open(file_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            a = json.loads(line.rstrip())[0]
            print("============ ", i, a['edit_type'], a['edit_indices'])
            found = False
            for j, (tag, i1, i2, j1, j2) in enumerate(extract_opcodes(a['text_original'], a['text_amended'])):
                print('\t', j, tag, i1, i2, j1, j2)
                if a['edit_type'] == tag and a['edit_indices'] == {"i1": i1, "i2": i2, "j1": j1, "j2": j2}:
                    print('Founded', j)
                    found = True
                    break
            if not found and i not in [18, 39, 40, 44]:
                print('Not found')
                print(set(extract_opcodes(a['text_original'], a['text_amended'])))
                to = a['text_original']
                ta = a['text_amended']
                print("original ::::: " + ' '.join(a['text_original']))
                print("amended  ::::: " + ' '.join(a['text_amended']))
                import IPython; IPython.embed()
                break

            print('-----')
            if i > 60:
                break
