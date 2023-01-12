import argparse
import ast
import json
from pathlib import Path

import pandas as pd


def main():
    out_mag = {}
    out_s2fos = {}
    out_s2fos_mag_fall_back = {}
    
    for decade in range(1950, 2030, 10):
        with open(DAT_DIR / f'out_mag_{args.q}_{decade}.json') as f:
            out_mag.update({ 
                ast.literal_eval(key): value for key, value in json.load(f).items() 
            })
        
        with open(DAT_DIR / f'out_s2fos_{args.q}_{decade}.json') as f:
            out_s2fos.update({ 
                ast.literal_eval(key): value for key, value in json.load(f).items() 
            })
        
        with open(DAT_DIR / f'out_s2fos_mag_fall_back_{args.q}_{decade}.json') as f:
            out_s2fos_mag_fall_back.update({ 
                ast.literal_eval(key): value for key, value in json.load(f).items() 
            })

    df_s2fos = pd.DataFrame(out_s2fos.keys(), columns=["field", "year"])\
                 .assign(n = lambda x: out_s2fos.values())
    
    df_mag = pd.DataFrame(out_mag.keys(), columns=["field", "year"])\
               .assign(n = lambda x: out_mag.values())
    
    df_s2fos_mag_fall_back = pd.DataFrame(out_s2fos_mag_fall_back.keys(), columns=["field", "year"])\
                               .assign(n = lambda x: out_s2fos_mag_fall_back.values())

    # left join because mag field are always in s2fos but not the other ways round
    df = df_s2fos.merge(df_mag, how="left", on=["field", "year"], suffixes=["_s2fos", "_mag"])\
                 .merge(df_s2fos_mag_fall_back, how="left", on=["field", "year"])\
                 .sort_values("year")

    soc_sci_and_humanities = ['Philosophy', 'Sociology', 'Economics', 'Political science', 'Geography', 'Linguistics', 'Psychology', 'History', 'Art']
    stem = ['Computer science', 'Physics', 'Materials science', 'Geology', 'Engineering', 'Chemistry', 'Environmental science', 'Biology', 'Mathematics']
    misc = ['Medicine', 'Business', 'Education', 'Agricultural and Food sciences', 'Law']

    fields_lookup = { f:'Social Science' for f in soc_sci_and_humanities }
    fields_lookup.update({ f:'STEM' for f in stem })
    fields_lookup.update({ f:'Misc' for f in misc })

    df['group'] = df.field.map(lambda x: fields_lookup[x])

    df.to_csv(f"count_field_and_decade_{args.q}.csv", index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", help = "q is either pdf, abstract, or all.")
    args = parser.parse_args()

    CURRENT_DIR = Path()
    DAT_DIR = CURRENT_DIR / 'out_files'

    main()