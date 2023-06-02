import json
from jsondiff import diff
from Levenshtein import distance



if __name__ == '__main__':
    originals = [json.loads(l) for l in open("from_zenodo_sorted.json").readlines()]
    new = [json.loads(l) for l in open("AGRI_AM(2017)607910_EN.docx.json").readlines()]


    min = 1000000
    current = None
    for n in new:
        d = distance(' '.join(n['text_amended']), ' '.join(originals[0]['text_amended']))
        if d < min:
            min = d
            current = n

    d = diff(originals[0], current)
    print(d)
    import IPython; IPython.embed()


