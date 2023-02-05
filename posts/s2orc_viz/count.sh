#!/bin/bash

echo counting abstract
seq 1950 10 2020 | parallel python count_by_field_and_decade.py --decade {} -q abstract && python count2csv.py -q abstract && rm -rf out_files

echo counting pdf
seq 1950 10 2020 | parallel python count_by_field_and_decade.py --decade {} -q pdf && python count2csv.py -q pdf && rm -rf out_files &&

echo counting all
seq 1950 10 2020 | parallel python count_by_field_and_decade.py --decade {} -q all && python count2csv.py -q all && rm -rf out_files

python -c 'import pandas as pd; d1=pd.read_csv("count_field_and_decade_abstract.csv").assign(parsing=lambda x: "abstract"); d2=pd.read_csv("count_field_and_decade_pdf.csv").assign(parsing=lambda x: "pdf"); d3=pd.read_csv("count_field_and_decade_all.csv").assign(parsing=lambda x: "all"); pd.concat([d1,d2,d3], axis=0).to_csv("count_field_and_decade.csv", index=False)'
