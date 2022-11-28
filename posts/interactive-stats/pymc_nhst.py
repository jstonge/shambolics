import matplotlib.pyplot as plt
import pandas as pd
import pymc3 as pm
import seaborn as sns

plt.style.use("seaborn-whitegrid")

# We have 15 female and 17 male who responded (trials). The female have responded
# yes 5 times, while the male have responded 7 times (successes). 
# What is the probability that male have earlier experience than female.

d = pd.read_csv("data_clean.csv").query("is_coder == 'coder'")

# Catego 2lvl ~ Catego 2lvl
indep_var = pd.Categorical(d["gender_binary"])
dep_var = pd.Categorical(d["first_line_code_before_18"])
crosstab = pd.crosstab(indep_var, dep_var, dropna=True)
trials = crosstab.sum(axis=1).tolist()
successes = crosstab["yes"].tolist()
gr1, gr2 = crosstab.index.tolist()

with pm.Model() as m1:
    p = pm.Uniform("p", shape=2)
    obs = pm.Binomial("y", n=trials, p=p, shape=2, observed=successes)
    diff_mk2_mk1 = pm.Deterministic("diff_gr2_gr1", p[1] - p[0]) # Do Mks2 are more deadlier than Mks1model
    trace = pm.sample(return_inferencedata=False)

samples_diff = pd.DataFrame({'val': trace.get_values("diff_gr2_gr1")})
samples_diff['gt_than_zero'] = samples_diff.val > 0

sns.displot(samples_diff, x='val', linewidth=0, alpha=0.7, hue='gt_than_zero', 
            kde=False, stat='probability', bins=150)
plt.xlabel(f"Posterior {gr2} - {gr1}")

print(f'Prob {gr2} is more duped than {gr1}: {(trace.get_values(f"diff_mk2_mk1") > 0).mean()}')