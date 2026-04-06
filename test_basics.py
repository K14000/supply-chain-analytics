import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("✅ All imports successful!")

# Try loading data
df = pd.read_csv('supply_chain.csv')
print(f"✅ Data loaded: {len(df)} products")
print(df.head())