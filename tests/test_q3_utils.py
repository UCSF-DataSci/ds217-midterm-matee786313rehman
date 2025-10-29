import pandas as pd
import numpy as np
from q3_data_utils import detect_missing, fill_missing, create_bins


def test_detect_missing():
    df = pd.DataFrame({'a': [1, None, 3], 'b': [None, None, 2]})
    m = detect_missing(df)
    assert m['a'] == 1
    assert m['b'] == 2


def test_fill_missing_mean():
    df = pd.DataFrame({'x': [1.0, None, 3.0]})
    out = fill_missing(df, 'x', strategy='mean')
    assert out['x'].isna().sum() == 0
    assert out.loc[1, 'x'] == 2.0


def test_create_bins():
    df = pd.DataFrame({'age': [10, 20, 40, 70]})
    out = create_bins(df, 'age', bins=[0,18,35,50,100], labels=['<18','18-34','35-49','50+'])
    assert out['age_binned'].dtype.name == 'category'
    assert str(out.loc[0, 'age_binned']) == '<18'
