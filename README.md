EuroParl-Amendment-Extract
===========================

This is a simple script to convert the amendments from the EP to JSON.
It follow the format define in that dataset https://zenodo.org/record/4709248#.YXesJS8itqs for the article War Of Word
https://github.com/indy-lab/war-of-words

## prerequisites

Build the MEPs dataset with the script 
`python3 meps.py`


## Debugger

To run the debugger we simply need to run 'streamlit run diff_visualizer.py', it will run the am labeler on the ep8 dataset and visualize the first error that it comes across. 


## Sequence matcher update

In diff.py there is now a extract_opcodes and extract_opcodes_v2. The v2 takes into account to merge consecutive 'replace' operations as well as 'delete' operations followed by a replace. We also display now at the end an accuracy metric that sort of roughly sketches the am labeler's performance. The accuracy is calculated by penalizing the algorithm for each edit that it gets wrong relative to the size / length of text that was attributed to the edit in question. With this evaluation metric we observed a high accuracy (99+ %) on the ep8 dataset. 


## Usage 

```python
from ep_amendment_extract import  extract_amendments

extract_amendments('file.docx')
```
