import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from q3_data_utils import load_data, clean_data, detect_missing, fill_missing, transform_types, create_bins, summarize_by_group
import pandas as pd

out_lines = []

df = load_data('data/clinical_trial_raw.csv')
out_lines.append(f'Loaded {len(df)} rows, {len(df.columns)} columns')

# Clean and inspect missing
_df_clean = clean_data(df)
missing = detect_missing(_df_clean)
out_lines.append('Missing values per column:')
out_lines.extend([f'{c}: {missing[c]}' for c in missing.index[:10]])

# Fill BMI with median and transform types
_df_filled = fill_missing(_df_clean, 'bmi', strategy='median')
_df_typed = transform_types(_df_filled, {'enrollment_date': 'datetime', 'age': 'numeric'})

# Create age bins and summarize by site
_df_binned = create_bins(_df_typed, 'age', bins=[0,18,35,50,65,100], labels=['<18','18-34','35-49','50-64','65+'])
summary = summarize_by_group(_df_binned, 'site', agg_dict={'age':'mean','bmi':'mean'})
out_lines.append('\nSummary (top 10 sites):')
out_lines.extend([str(x) for x in summary.head(10).to_string().splitlines()])

# Save outputs
out_dir = repo_root / 'output'
reports_dir = repo_root / 'reports'
out_dir.mkdir(parents=True, exist_ok=True)
reports_dir.mkdir(parents=True, exist_ok=True)

summary.to_csv(out_dir / 'q4_site_summary.csv')
df['site'].value_counts().to_csv(out_dir / 'q4_site_counts.csv')
out_lines.append('\nWrote output/q4_site_summary.csv and output/q4_site_counts.csv')

with open(reports_dir / 'q3_demo.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print('\n'.join(out_lines))
