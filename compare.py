import json
from jsondiff import diff
from Levenshtein import distance



if __name__ == '__main__':
    originals = [json.loads(l) for l in open("from_zenodo_sorted.json").readlines()]
    new = [json.loads(l) for l in open("AGRI_AM(2017)607910_EN.docx.json").readlines()]

    min = 1000000
    current = None
    for n in new:
        if n['justification']:
           d = distance(n['justification'], originals[1]['justification'])
           if d < min:
               min = d
               current = n

    jd = diff(originals[1], current, syntax='symmetric')
    print(jd)
    import IPython; IPython.embed()


