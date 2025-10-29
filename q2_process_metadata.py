#!/usr/bin/env python3
# Assignment 5, Question 2: Python Data Processing
# Process configuration files for data generation.

import os
import random
import statistics
from typing import List, Dict


def parse_config(filepath: str) -> dict:
    """
    Parse config file (key=value format) into dictionary.

    Args:
        filepath: Path to q2_config.txt

    Returns:
        dict: Configuration as key-value pairs

    Example:
        >>> config = parse_config('q2_config.txt')
        >>> config['sample_data_rows']
        '100'
    """
    config = {}
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            config[key.strip()] = val.strip()
    return config


def validate_config(config: dict) -> dict:
    """
    Validate configuration values using if/elif/else logic.

    Rules:
    - sample_data_rows must be an int and > 0
    - sample_data_min must be an int and >= 1
    - sample_data_max must be an int and > sample_data_min

    Args:
        config: Configuration dictionary

    Returns:
        dict: Validation results {key: True/False}

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> results = validate_config(config)
        >>> results['sample_data_rows']
        True
    """
    results = {}

    # sample_data_rows
    val = config.get('sample_data_rows')
    try:
        n = int(val)
        if n > 0:
            results['sample_data_rows'] = True
        else:
            results['sample_data_rows'] = False
    except Exception:
        results['sample_data_rows'] = False

    # sample_data_min
    val = config.get('sample_data_min')
    try:
        mn = int(val)
        if mn >= 1:
            results['sample_data_min'] = True
        else:
            results['sample_data_min'] = False
    except Exception:
        results['sample_data_min'] = False

    # sample_data_max
    val = config.get('sample_data_max')
    try:
        mx = int(val)
        # must be greater than min
        if 'sample_data_min' in config:
            try:
                mn = int(config['sample_data_min'])
            except Exception:
                mn = None
        else:
            mn = None
        if mn is not None and mx > mn:
            results['sample_data_max'] = True
        else:
            results['sample_data_max'] = False
    except Exception:
        results['sample_data_max'] = False

    return results


def generate_sample_data(filename: str, config: dict) -> None:
    """
    Generate a file with random numbers for testing, one number per row with no header.
    Uses config parameters for number of rows and range.

    Args:
        filename: Output filename (e.g., 'sample_data.csv')
        config: Configuration dictionary with sample_data_rows, sample_data_min, sample_data_max

    Returns:
        None: Creates file on disk

    Example:
        >>> config = {'sample_data_rows': '100', 'sample_data_min': '18', 'sample_data_max': '75'}
        >>> generate_sample_data('sample_data.csv', config)
        # Creates file with 100 random numbers between 18-75, one per row
        >>> import random
        >>> random.randint(18, 75)  # Returns random integer between 18-75
    """
    # Parse config values
    rows = int(config['sample_data_rows'])
    mn = int(config['sample_data_min'])
    mx = int(config['sample_data_max'])

    # Ensure output directory exists
    outdir = os.path.dirname(filename)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(rows):
            r = random.randint(mn, mx)
            f.write(f"{r}\n")



def calculate_statistics(data: list) -> dict:
    """
    Calculate basic statistics.

    Args:
        data: List of numbers

    Returns:
        dict: {mean, median, sum, count}

    Example:
        >>> stats = calculate_statistics([10, 20, 30, 40, 50])
        >>> stats['mean']
        30.0
    """
    if not data:
        return {'mean': None, 'median': None, 'sum': 0, 'count': 0}
    cnt = len(data)
    s = sum(data)
    mean = statistics.mean(data)
    median = statistics.median(data)
    return {'mean': mean, 'median': median, 'sum': s, 'count': cnt}


if __name__ == '__main__':
    # End-to-end execution
    cfg_file = 'q2_config.txt'
    out_csv = 'data/sample_data.csv'
    stats_file = 'output/statistics.txt'

    print(f"Reading config from {cfg_file}...")
    cfg = parse_config(cfg_file)
    print("Validating config...")
    results = validate_config(cfg)
    print(results)

    # If any validation failed, report and exit
    if not all(results.values()):
        failed = [k for k, v in results.items() if not v]
        print(f"Config validation failed for: {failed}")
        raise SystemExit(1)

    print(f"Generating sample data at {out_csv}...")
    generate_sample_data(out_csv, cfg)

    # Read generated data
    with open(out_csv, 'r', encoding='utf-8') as f:
        nums = [int(line.strip()) for line in f if line.strip()]

    stats = calculate_statistics(nums)
    print("Calculated statistics:", stats)

    # Ensure output dir
    os.makedirs(os.path.dirname(stats_file), exist_ok=True)
    with open(stats_file, 'w', encoding='utf-8') as f:
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")

    print(f"Wrote statistics to {stats_file}")
