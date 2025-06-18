import pandas as pd
from scipy.stats import kstest

def is_significant_defect_matrix(df: pd.DataFrame, p_threshold: float = 0.20) -> bool:
    """
    Applies KS test column-wise to determine if any column in the matrix
    is statistically different from a normal distribution.

    :param df: The defect submatrix (DataFrame)
    :param p_threshold: Significance level to detect non-normality
    :return: True if statistically significant, else False
    """
    for col in df.columns:
        col_data = df[col].dropna().values
        if len(col_data) > 5:
            stat, p = kstest(col_data, 'norm')
            if p < p_threshold:
                return True  # At least one column is significantly different
    return False
