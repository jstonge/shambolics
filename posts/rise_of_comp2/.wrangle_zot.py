import re
import sys

import pandas as pd


def extract_paper_id(d):
    d['Notes'] = d.Notes.map(lambda x: re.split(";", x)[0])
    d['Notes'] = d.Notes.map(lambda x: re.split("\.", x)[1])
    d = d.rename(columns={'Notes': 'paper_id'})
    return d

def wrangle_tags_into_cols(d):
    d['Manual Tags'] = d['Manual Tags'].str.split("; ")
    d = d.explode('Manual Tags')
    d = d.reset_index(drop=True)
    d[['type_catego', 'main_cat', 'sub_cat']] = d['Manual Tags'].str.split("\.", expand=True)
    d = d.drop('Manual Tags', axis=1)
    return d

def extract_inst_and_lab(d):
    tmp_inst = d.set_index('paper_id')['inst'].str.split(", ").explode()
    tmp_type1 = d.set_index('paper_id')['type1'].str.split(", ").explode()
    d_loc = pd.merge(tmp_inst, tmp_type1, left_index=True, right_index=True).reset_index()
    d = d_loc.merge(d[['paper_id', 'lab']], how='left', on='paper_id')
    return d

def main():
    """
    Grab institutions and programming labels from my Zotero file. 
    """
    d = pd.read_csv(sys.argv[1], usecols= ['Notes', 'Manual Tags'])

    d = extract_paper_id(d)
    d = wrangle_tags_into_cols(d)

    # keep only relevant labs
    d = d[d.type_catego.isin(['type', 'inst', 'lab', 'loc'])]

    # pivot
    d = d.pivot_table(index='paper_id', columns='type_catego', aggfunc= lambda x: ', '.join(x)).reset_index()
    d.columns = ['paper_id']+list(d.columns.get_level_values(1)[1:-2])+['type1', 'type2']

    # extract from lab, inst, type1
    d = extract_inst_and_lab(d)

    d.to_csv("classify-comp-proj-tidy.csv", index=False)


main()