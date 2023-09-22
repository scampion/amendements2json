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
            am_mistake_found = False
            # Bookkeeping
            amount_amendments += 1
            score = 1
            #print(f'amendment {i}:')

            for j, (tag, i1, i2, j1, j2) in enumerate(extract_opcodes(a['text_original'], a['text_amended'])):
                # print('\t', j, tag, i1, i2, j1, j2)
                if a['edit_type'] == tag and a['edit_indices'] == {"i1": i1, "i2": i2, "j1": j1, "j2": j2}:
                    #print('Found', j)
                    found = True
                    break

            if not found:
                i1, i2 = a["edit_indices"]["i1"], a["edit_indices"]["i2"]
                score -= (i2 - i1) / len(a['text_amended'])
                am_mistake_found = True
                print(f'Mistake found with type {a["edit_type"]} and indices {a["edit_indices"]}.')

            total_score += score

            if am_mistake_found:
                print("Amendment mistake found")
                amendments_with_mistakes += 1

        print('-----')

    print(f"Total score is {total_score} with {amount_amendments} amendments with {amendments_with_mistakes} containing"
          f" some type of edit mistakes, score is {total_score / amount_amendments}")
