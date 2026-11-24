import pandas as pd
from pathlib import Path
from scipy import stats

data_dir = Path("data")
N_TRIALS = 95
BLOCK = 19

# Payoff scheme per study, from Table 1 of the data paper
SCHEME = {
    "Fridberg": 1, "Maia": 1, "Worthy": 1,
    "Horstmann": 2, "Steingroever2011": 2, "SteingroverInPrep": 2, "Wetzels": 2,
    "Kjome": 3, "Premkumar": 3, "Wood": 3,
}

# Load and compute block scores (same as script 02)
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
print("Participants without a scheme:", blocks["Scheme"].isna().sum())

# 1. Block 5 vs block 1 (paired)
b1, b5 = blocks["block_1"], blocks["block_5"]
t, p = stats.ttest_rel(b5, b1)
diff = b5 - b1
dz = diff.mean() / diff.std(ddof=1)
print(f"\nBlock 5 vs block 1: t({len(diff) - 1}) = {t:.2f}, p = {p:.3g}, dz = {dz:.2f}")

# 2. Block 5 vs chance
t, p = stats.ttest_1samp(b5, 0.5)
print(f"Block 5 vs chance (0.5): t({len(b5) - 1}) = {t:.2f}, p = {p:.3g}")

# 3. Block 5 across payoff schemes
groups = [g["block_5"].values for _, g in blocks.groupby("Scheme")]
F, p = stats.f_oneway(*groups)
print(f"\nBlock 5 by payoff scheme: F = {F:.2f}, p = {p:.3g}")
print(blocks.groupby("Scheme")["block_5"].agg(["count", "mean", "std"]).round(2))

res = stats.tukey_hsd(*groups)
print(res)