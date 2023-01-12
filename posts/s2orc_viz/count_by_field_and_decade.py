import argparse
import json
import re
from pathlib import Path

from jsonlines import jsonlines


def main():
    """
    GET NUMBER PAPER BY YEAR AND FIELD

    Return a dictionary object whereas the key is a tupple (field, year)
    and the value is the count number.
    """
    CURRENT_DIR = Path()
    OUT_DIR = CURRENT_DIR / 'out_files'
    HARDDRIVE_DIR = Path("/media/jstonge/Back_up/s2orc")
    DIR_METADATA_BY_DECADE = HARDDRIVE_DIR / 'metadata_by_decade_all'

    if OUT_DIR.exists() == False: OUT_DIR.mkdir()

    print(args.q)
    
    # q = 'all'
    fnames = list(DIR_METADATA_BY_DECADE.glob(f"*{args.q}.jsonl"))
    
    # decade = "1950"
    fname = [_ for _ in fnames if re.search(args.decade, str(_))][0]
    
    mag_field = 'mag_field_of_study' if args.q == 'all' else 'mag_field'
    s2_field = 's2_field_of_study' if args.q == 'all' else 's2_field'

    out_mag = {}
    out_s2fos = {}
    out_s2fos_mag_fall_back = {}

    with jsonlines.open(fname) as f:
        for line in f:
            
            # magfield is a simple list 
            if line.get(mag_field) is not None:
            
                for field in line[mag_field]:
                    if out_mag.get((field, line['year'])) is None:
                        out_mag[(field, line['year'])] = 1
                    else:
                        out_mag[(field, line['year'])] += 1

                # s2fos is a list of dictionaries
                if line[s2_field] is not None:
                    
                    for field in line[s2_field]:
                        if out_s2fos.get((field, line['year'])) is None:
                            out_s2fos[(field, line['year'])] = 1
                        else:
                            out_s2fos[(field, line['year'])] += 1
        
                # Keyword search in API by year and field returns any paper from fiel
                # containing a hit from the search algorithm. But on the website, I t
                # consider the s2orc classification, then falls back on the mag_field
                # e.g. if s2field is not None s2field == 'Art' else is mag_field == '
                # we need to do something similar.
                if line[s2_field] is not None:
                    for field in line[s2_field]:
                        if out_s2fos_mag_fall_back.get((field, line['year'])) is None:
                            out_s2fos_mag_fall_back[(field, line['year'])] = 1
                        else:
                            out_s2fos_mag_fall_back[(field, line['year'])] += 1
                else:
                    for field in line[mag_field]:
                        if out_s2fos_mag_fall_back.get((field, line['year'])) is None:
                            out_s2fos_mag_fall_back[(field, line['year'])] = 1
                        else:
                            out_s2fos_mag_fall_back[(field, line['year'])] += 1

    out_mag = {str(key): value for key, value in out_mag.items()}
    out_s2fos = {str(key): value for key, value in out_s2fos.items()}
    out_s2fos_mag_fall_back = {str(key): value for key, value in out_s2fos_mag_fall_back.items()}

    with open(OUT_DIR / f'out_mag_{args.q}_{args.decade}.json', "w") as f:
        json.dump(out_mag, f)
     
    with open(OUT_DIR / f'out_s2fos_{args.q}_{args.decade}.json', "w") as f:
        json.dump(out_s2fos, f)

    with open(OUT_DIR / f'out_s2fos_mag_fall_back_{args.q}_{args.decade}.json', "w") as f:
        json.dump(out_s2fos_mag_fall_back, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--decade")
    parser.add_argument("-q", help = "q is either pdf, abstract, or all.")
    args = parser.parse_args()

    main()