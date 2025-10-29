from pathlib import Path
import sys
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
from q3_data_utils import load_data, filter_data

reports_dir = repo_root / 'reports'
reports_dir.mkdir(parents=True, exist_ok=True)

fpath = repo_root / 'data' / 'clinical_trial_raw.csv'
df = load_data(str(fpath))

out = []
# Patients over 65
filters = [{'column': 'age', 'condition': 'greater_than', 'value': 65}]
patients_over_65 = filter_data(df, filters)
out.append(f'Patients over 65: {len(patients_over_65)}')

# Patients with systolic_bp > 140
filters = [{'column': 'systolic_bp', 'condition': 'greater_than', 'value': 140}]
high_bp = filter_data(df, filters)
out.append(f'Patients with systolic BP > 140: {len(high_bp)}')

# Both conditions
filters = [
    {'column': 'age', 'condition': 'greater_than', 'value': 65},
    {'column': 'systolic_bp', 'condition': 'greater_than', 'value': 140}
]
both = filter_data(df, filters)
out.append(f'Patients over 65 AND systolic BP > 140: {len(both)}')

# Site A/B variants (original)
site_candidates = [s for s in df['site'].dropna().unique() if 'SITE A' in str(s).upper() or 'SITE B' in str(s).upper()]
filters = [{'column': 'site', 'condition': 'in_list', 'value': list(site_candidates)}]
site_ab = filter_data(df, filters)
out.append(f'Patients from Site A or Site B (filter_data in_list, variants): {len(site_ab)}')
out.append(f'Matched site variants: {site_candidates}')

# Site A/B using .isin() on cleaned site text (recommended)
df['site_clean'] = df['site'].astype(str).str.strip().str.upper()
site_values = ['SITE A', 'SITE B']
site_ab_isin = df[df['site_clean'].isin(site_values)]
out.append(f'Patients from Site A or Site B (isin on cleaned values): {len(site_ab_isin)}')

print('\n'.join(out))
with open(reports_dir / 'q4_filters.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(out))
