#!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library
# Core reusable functions for data loading, cleaning, and transformation.

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.
    """
    if not isinstance(filepath, str):
        raise TypeError('filepath must be a string')
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True, 
               sentinel_value: Union[float, int] = -999) -> pd.DataFrame:
    """
    Basic data cleaning: remove duplicates, replace sentinel values, and aggressively 
    standardize string columns, including fixing known misspellings with a final 
    explicit mapping.
    """
    out = df.copy()

    # 1. Remove duplicates
    if remove_duplicates:
        out.drop_duplicates(inplace=True)

    # 2. Replace sentinel values with NaN (np.nan)
    out.replace(to_replace=[sentinel_value, -1], value=np.nan, inplace=True)
    
    # --- Final Aggressive Mapping Dictionary for Ultimate Consolidation ---
    # This dictionary maps ALL observed fragmented values (in UPPER case) 
    # to the final, clean target groups.
    CONSOLIDATED_MAPPING = {
        # Site Consolidation (Targets: Site A, B, C, D, E)
        'SITE A': 'Site A', 'SITE B': 'Site B', 'SITE C': 'Site C', 
        'SITE D': 'Site D', 'SITE E': 'Site E', 'SITE_D': 'Site D',

        # Intervention Group Consolidation (Targets: Control, Intervention)
        # All control variations
        'CONTROL': 'Control', 'CONTRL': 'Control', 'CONTROL GROUP': 'Control',
        
        # All treatment variations (A and B) consolidated into 'Intervention'
        'TREATMENT A': 'Intervention', 'TREATMENTB': 'Intervention', 
        'TREATMEN A': 'Intervention', 'TREATMENTB ': 'Intervention',
        'TREATMENT B': 'Intervention', 'TREATMENTA': 'Intervention', 
    }
    
    # 3. Apply Standardization and Final Mapping
    for col in ['site', 'intervention_group', 'sex', 'outcome_cvd', 'dropout']:
        if col in out.columns:
            # Step A: Aggressive Text Cleaning
            # Use UPPERCASE for easy, non-case-sensitive matching in the dictionary
            out[col] = out[col].astype(str).str.normalize('NFKC').str.upper()
            out[col] = out[col].str.replace('_', ' ', regex=False).str.strip()
            out[col] = out[col].str.replace(r'[^A-ZA-Z\s]', '', regex=True).str.strip() 
            out[col] = out[col].str.replace(r'\s+', ' ', regex=True).str.strip()
            out[col] = out[col].replace('NAN', np.nan) # Replace NaN strings created by cleaning
            
            # Step B: Apply final explicit mapping to the now-UPPERCASE strings
            # This is the guaranteed fix for the fragmentation
            out[col] = out[col].replace(CONSOLIDATED_MAPPING)
            
            # Step C: Re-apply Title Case to clean columns for final output readability
            if col not in ['site', 'intervention_group']: # Only apply to other categorical
                out[col] = out[col].str.title() 

    return out


def detect_missing(df: pd.DataFrame) -> pd.Series:
    """
    Count missing values (NaN or NaT) per column.
    """
    return df.isnull().sum().rename('missing_count')


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    """
    Fill missing values in a column using specified strategy.
    """
    out = df.copy()
    if column not in out.columns:
        raise KeyError(f"Column not found: {column}")
        
    if strategy == 'ffill':
        out[column] = out[column].fillna(method='ffill')
        return out
        
    if strategy in ['mean', 'median']:
        if not pd.api.types.is_numeric_dtype(out[column]):
            raise TypeError(f"Cannot use '{strategy}' on non-numeric column: {column}")
            
        if strategy == 'mean':
            val = out[column].dropna().mean()
        elif strategy == 'median':
            val = out[column].dropna().median()
            
        out[column] = out[column].fillna(val)
        return out
    else:
        raise ValueError('Unsupported strategy: choose mean, median, or ffill')


def filter_data(df: pd.DataFrame, filters: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Apply a list of filters to DataFrame in sequence.
    """
    out = df.copy()
    for f in filters:
        col = f.get('column')
        cond = f.get('condition')
        val = f.get('value')
        
        if col not in out.columns:
            continue
            
        if pd.api.types.is_numeric_dtype(out[col]) and not pd.api.types.is_numeric_dtype(type(val)):
             out[col] = pd.to_numeric(out[col], errors='coerce')


        if cond == 'equals':
            out = out[out[col] == val]
        elif cond == 'greater_than':
            out = out[out[col] > val]
        elif cond == 'less_than':
            out = out[out[col] < val]
        elif cond == 'in_range':
            if not isinstance(val, (list, tuple)) or len(val) != 2:
                raise ValueError("in_range filter requires a list/tuple of [low, high]")
            lo, hi = val
            out = out[(out[col] >= lo) & (out[col] <= hi)]
        elif cond == 'in_list':
            out = out[out[col].isin(val)]
        else:
            raise ValueError(f'Unsupported condition: {cond}')
            
    return out.reset_index(drop=True)


def transform_types(df: pd.DataFrame, type_map: Dict[str, str]) -> pd.DataFrame:
    """
    Convert column data types based on mapping.
    """
    out = df.copy()
    for col, t in type_map.items():
        if col not in out.columns:
            continue
        if t == 'datetime':
            out[col] = pd.to_datetime(out[col], errors='coerce', format='mixed')
        elif t == 'numeric':
            out[col] = pd.to_numeric(out[col], errors='coerce')
        elif t == 'category':
            out[col] = out[col].astype(str).astype('category')
        elif t == 'string':
            out[col] = out[col].astype(str)
        else:
            out[col] = out[col].astype(t)
            
    return out


def create_bins(df: pd.DataFrame, column: str, bins: List[Any], 
                labels: List[str], new_column: str = None) -> pd.DataFrame:
    """
    Create categorical bins from continuous data using pd.cut().
    """
    out = df.copy()
    if new_column is None:
        new_column = f"{column}_binned"
        
    if column not in out.columns:
        raise KeyError(f'Bin column not found: {column}')
        
    out[new_column] = pd.cut(out[column], 
                             bins=bins, 
                             labels=labels, 
                             include_lowest=True, 
                             right=True)
    return out


def summarize_by_group(df: pd.DataFrame, group_col: str, 
                       agg_dict: Dict[str, Union[str, List[str]]] = None) -> pd.DataFrame:
    """
    Group data and apply aggregations, adding a patient count if not specified.
    """
    if group_col not in df.columns:
        raise KeyError(f'Group column not found: {group_col}')
        
    if agg_dict is None:
        summary_df = df.groupby(group_col).size().to_frame(name='patient_count').reset_index()
        return summary_df
    else:
        summary_df = df.groupby(group_col).agg(agg_dict)
        
        if 'patient_count' not in summary_df.columns:
              count_df = df.groupby(group_col).size().rename('patient_count')
              summary_df = summary_df.join(count_df)

        return summary_df.reset_index()


if __name__ == '__main__':
    print("Data utilities loaded successfully!")