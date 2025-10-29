import pandas as pd
import numpy as np
from q3_data_utils import load_data, detect_missing, fill_missing

# Load data
df = load_data('data/clinical_trial_raw.csv')
print(f'Loaded {len(df)} rows, {len(df.columns)} columns')

# Part 2: imputation comparison for cholesterol_total
col = 'cholesterol_total'
orig_mean = df[col].mean()
orig_median = df[col].median()
orig_na = df[col].isna().sum()

# mean fill
df_mean = df.copy()
df_mean = fill_missing(df_mean, col, strategy='mean')
mean_after_mean = df_mean[col].mean()
na_after_mean = df_mean[col].isna().sum()

# median fill
df_median = df.copy()
df_median = fill_missing(df_median, col, strategy='median')
mean_after_median = df_median[col].mean()
na_after_median = df_median[col].isna().sum()

# ffill
df_ffill = df.copy()
df_ffill[col] = df_ffill[col].fillna(method='ffill')
na_after_ffill = df_ffill[col].isna().sum()

print('Imputation for', col)
print('orig mean, median, na:', orig_mean, orig_median, orig_na)
print('after mean fill: mean, na:', mean_after_mean, na_after_mean)
print('after median fill: mean, na:', mean_after_median, na_after_median)
print('after ffill: mean, na:', df_ffill[col].mean(), na_after_ffill)

# Part 3: drop strategies
rows_any = df.dropna()
rows_age_bmi = df.dropna(subset=['age','bmi'])
print('\nDrop any NA remaining rows:', len(rows_any))
print("Drop age/bmi NA remaining rows:", len(rows_age_bmi))

# Part 4: create cleaned dataset
df_clean = df.copy()
# drop critical
if 'patient_id' in df_clean.columns and 'age' in df_clean.columns:
    df_clean = df_clean.dropna(subset=['patient_id','age'])
# median fill for specific
for c in ['bmi','cholesterol_total','cholesterol_hdl','cholesterol_ldl']:
    if c in df_clean.columns:
        df_clean = fill_missing(df_clean, c, strategy='median')
# mean for other numeric
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
for c in numeric_cols:
    if c not in ['bmi','cholesterol_total','cholesterol_hdl','cholesterol_ldl','patient_id','age']:
        df_clean = fill_missing(df_clean, c, strategy='mean')
# ffill remaining
df_clean = df_clean.fillna(method='ffill')

# save
missing_before = detect_missing(df)
missing_after = detect_missing(df_clean)
missing_report = pd.DataFrame({'missing_before': missing_before, 'missing_after': missing_after})

df_clean.to_csv('output/q5_cleaned_data.csv', index=False)
missing_report.to_csv('output/q5_missing_report.txt', sep='\t')
print('\nWrote output/q5_cleaned_data.csv and output/q5_missing_report.txt')
print('\nRemaining missing columns:', missing_after[missing_after>0])
