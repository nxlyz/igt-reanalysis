import pandas as pd
from pathlib import Path
import statsmodels.formula.api as smf

data_dir = Path("data")
N_TRIALS = 95
BLOCK = 19

SCHEME = {
    "Fridberg": 1, "Maia": 1, "Worthy": 1,
    "Horstmann": 2, "Steingroever2011": 2, "SteingroverInPrep": 2, "Wetzels": 2,
    "Kjome": 3, "Premkumar": 3, "Wood": 3,
}

# Load and compute block scores (same as scripts 02 and 03)
frames = []
for n in [95, 100, 150]:
    choice = pd.read_csv(data_dir / f"choice_{n}.csv")
    index = pd.read_csv(data_dir / f"index_{n}.csv")
    choice = choice.iloc[:, :N_TRIALS].copy()
    choice["Study"] = index["Study"].values
    frames.append(choice)
all_choices = pd.concat(frames, ignore_index=True)

trial_cols = [f"Choice_{i}" for i in range(1, N_TRIALS + 1)]
good = all_choices[trial_cols].isin([3, 4])
blocks = pd.DataFrame({
    f"block_{b + 1}": good.iloc[:, b * BLOCK:(b + 1) * BLOCK].mean(axis=1)
    for b in range(N_TRIALS // BLOCK)
})
blocks["Study"] = all_choices["Study"]
blocks["Scheme"] = blocks["Study"].map(SCHEME)
blocks["gain"] = blocks["block_5"] - blocks["block_1"]

# Model 1: learning gain, with a random intercept for study
m1 = smf.mixedlm("gain ~ 1", blocks, groups=blocks["Study"]).fit(reml=True)
print("MODEL 1: gain from block 1 to block 5")
print(m1.summary())
print("95% CI for the average gain:")
print(m1.conf_int().loc["Intercept"].round(3))

# Model 2: block 5 by payoff scheme, with a random intercept for study
m2 = smf.mixedlm("block_5 ~ C(Scheme)", blocks, groups=blocks["Study"]).fit(reml=True)
print("\nMODEL 2: block 5 by payoff scheme")
print(m2.summary())
print("95% CIs:")
print(m2.conf_int().round(3))

# How much of the variation in block 5 sits between studies?
m0 = smf.mixedlm("block_5 ~ 1", blocks, groups=blocks["Study"]).fit(reml=True)
icc = m0.cov_re.iloc[0, 0] / (m0.cov_re.iloc[0, 0] + m0.scale)
print(f"\nShare of block 5 variance between studies (ICC): {icc:.3f}")