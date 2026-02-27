import numpy as np
import pandas as pd

np.random.seed(42)
n = 2000
base = 100 + np.cumsum(np.random.normal(0, 0.08, n))
spread_a = np.random.uniform(0.03, 0.12, n)
spread_b = np.random.uniform(0.03, 0.12, n)
edge = np.random.normal(0.05, 0.12, n)  # bの方が高い瞬間を含む

rows = []
for i in range(n):
    a_mid = base[i]
    b_mid = base[i] + edge[i]

    a1 = a_mid + spread_a[i] / 2
    b1 = b_mid - spread_b[i] / 2

    rows.append(
        {
            "a1_price": round(a1, 4),
            "a1_size": round(np.random.uniform(0.4, 1.5), 4),
            "a2_price": round(a1 * 1.001, 4),
            "a2_size": round(np.random.uniform(0.8, 2.0), 4),
            "b1_price": round(b1, 4),
            "b1_size": round(np.random.uniform(0.4, 1.5), 4),
            "b2_price": round(b1 * 0.999, 4),
            "b2_size": round(np.random.uniform(0.8, 2.0), 4),
            "stale_seconds": round(max(0, np.random.normal(0.4, 0.35)), 4),
        }
    )

pd.DataFrame(rows).to_csv("data/sample_market.csv", index=False)
print("generated: data/sample_market.csv")
