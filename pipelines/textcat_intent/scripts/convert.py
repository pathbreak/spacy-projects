"""Convert textcat annotation from CSV to spaCy v3 .spacy format."""
import warnings
from pathlib import Path
import typer

import csv
import json
import sys
import spacy
from spacy.tokens import DocBin


def convert(input_path: Path, cats_json:Path, output_path: Path):
    
    
    with open(cats_json, 'r') as f:
        cats = json.load(f)
        
    one_hot_dicts = {}
    for c in cats:
        one_hot_dict = {t:(1 if t==c else 0) for t in cats }
        one_hot_dicts[c] = one_hot_dict
        

    nlp = spacy.blank('en')
    
    db = DocBin()
    
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        
        hdr = next(reader)
        
        for row in reader:
            text = row[0]
            cat = row[1]
            
            doc = nlp.make_doc(text)
            doc.cats = one_hot_dict[cat]
            db.add(doc)

    db.to_disk(output_path)


if __name__ == "__main__":
    typer.run(convert)
