from pathlib import Path
import re
import pandas as pd
import numpy as np

s2orc_path = Path("/media/jstonge/Back_up/s2orc/classify_comp_proj/raw_dat/")

d = pd.read_csv("count_field_and_decade.csv")
d['field'] = d.field.str.lower()

fnames = list(s2orc_path.glob("*pqt"))

dfs = []
for fname in fnames:
    field_ = re.sub("(computational|-|.pqt)", "", str(fname).split("/")[-1])
    dfs.append(pd.read_parquet(fname).assign(field = lambda x: field_))

dfs = pd.concat(dfs, axis=0)

dfs['field'] = dfs.field.str.lower()
df_count_comp = dfs.value_counts(["field", "year"]).reset_index(name="n_comp")

new_df = d.merge(df_count_comp, how="left", on=["year","field"]).query('year < 2020')

new_df['pct_comp'] = new_df.n_comp / new_df.n

# new_df['group'] = np.where(new_df.field == 'psychology', 'MISC', new_df.group)

new_df = new_df[~new_df.pct_comp.isnull()]

new_df_abstract = new_df.query('parsing == "abstract"')

new_df_abstract.to_csv("comp_normalized.csv", index=False)