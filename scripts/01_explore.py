import pandas as pd
from pathlib import Path

data_dir = Path("data")

for n in [95, 100, 150]:
    choice = pd.read_csv(data_dir / f"choice_{n}.csv")
    index = pd.read_csv(data_dir / f"index_{n}.csv")
    print(f"--- {n}-trial files ---")
    print("shape (participants x trials):", choice.shape)
    print(choice.iloc[:3, :10])
    print(index.iloc[:, 0].value_counts())
