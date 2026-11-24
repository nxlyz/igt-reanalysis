import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data_dir = Path("data")
fig_dir = Path("figures")
N_TRIALS = 95
BLOCK = 19

# Load all three groups and keep the first 95 trials
frames = []
for n in [95, 100, 150]:
    choice = pd.read_csv(data_dir / f"choice_{n}.csv")
    index = pd.read_csv(data_dir / f"index_{n}.csv")
    choice = choice.iloc[:, :N_TRIALS].copy()
    choice["Study"] = index["Study"].values
    frames.append(choice)

all_choices = pd.concat(frames, ignore_index=True)
print("Participants:", len(all_choices))

# Good decks are C and D (coded 3 and 4)
trial_cols = [f"Choice_{i}" for i in range(1, N_TRIALS + 1)]
good = all_choices[trial_cols].isin([3, 4])

# Proportion of good deck choices per block, per participant
blocks = pd.DataFrame({
    f"block_{b + 1}": good.iloc[:, b * BLOCK:(b + 1) * BLOCK].mean(axis=1)
    for b in range(N_TRIALS // BLOCK)
})
blocks["Study"] = all_choices["Study"]
block_cols = [c for c in blocks.columns if c.startswith("block_")]

# Summaries
print("\nMean proportion of good choices per block:")
print(blocks[block_cols].mean().round(3))
print("\nBy study:")
print(blocks.groupby("Study")[block_cols].mean().round(2))

# Plot
mean_curve = blocks[block_cols].mean()
sem = blocks[block_cols].sem()
x = list(range(1, len(block_cols) + 1))

plt.errorbar(x, mean_curve, yerr=sem, marker="o", capsize=3)
plt.axhline(0.5, linestyle="--", color="grey")
plt.xlabel(f"Block ({BLOCK} trials each)")
plt.ylabel("Proportion of good deck choices (C + D)")
plt.title(f"IGT learning curve, all participants (N = {len(blocks)})")
plt.xticks(x)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(fig_dir / "learning_curve_all.png", dpi=200)
print("\nSaved figures/learning_curve_all.png")
