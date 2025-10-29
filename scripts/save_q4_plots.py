import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

import pandas as pd
import matplotlib.pyplot as plt
from q3_data_utils import load_data

# Load data
df = load_data('data/clinical_trial_raw.csv')

# Plot site counts
site_counts = df['site'].value_counts()
plt.figure(figsize=(10,6))
site_counts.plot(kind='bar')
plt.title('Site value counts')
plt.xticks(rotation=45)
plt.tight_layout()
reports_dir = repo_root / 'reports'
reports_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(reports_dir / 'q4_site_counts.png')
plt.close()

# Crosstab heatmap
crosstab = pd.crosstab(df['site'], df['intervention_group'])
plt.figure(figsize=(10,8))
plt.imshow(crosstab.values, cmap='Blues', aspect='auto')
plt.colorbar()
plt.title('Site x Intervention crosstab')
plt.xticks(range(len(crosstab.columns)), crosstab.columns, rotation=45)
plt.yticks(range(len(crosstab.index)), crosstab.index)
plt.tight_layout()
plt.savefig(reports_dir / 'q4_crosstab.png')
plt.close()

print('Saved reports/q4_site_counts.png and reports/q4_crosstab.png')
