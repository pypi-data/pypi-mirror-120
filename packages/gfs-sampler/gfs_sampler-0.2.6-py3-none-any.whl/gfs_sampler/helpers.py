"""
This file is part of gfs_sampler.

gfs_sampler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gfs_sampler is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gfs_sampler. If not, see <https://www.gnu.org/licenses/>.
"""

import numpy as np
import pandas as pd
import math
from scipy.stats import norm
    
def apply_permutation(df1, df2, permutation, block = "block"):
    """
    Apply a permuation to obtain a full linked data set from df1 and df2.
    The permutation is applied to df2, reordering its rows with respect to df1.
    
    df1: The first dataframe.
    df2: The second dataframe.
    permutation: The permutation to apply.
    """
    if block in df1.columns:
        df1 = df1.drop(block, axis=1)
    if block in df2.columns:
        df2 = df2.drop(block, axis=1)
    p = np.array(permutation)
    if len(p.shape) != 1 or (len(p.shape) == 2 and p.shape[1] != 1):
        raise ValueError("permuation argument must contain a single permutation (row or column).")
    if len(p) != df1.shape[0]:
        raise ValueError("permuation must contain the same number of rows as the df1 input (including row exclusions indicated by NaN).")
    df1_adj = df1.loc[np.isfinite(p)].reset_index(drop = True)
    df2_unshuffled = df2.loc[p[np.isfinite(p)]].reset_index(drop = True)
    permuted_df = pd.concat([df1_adj, df2_unshuffled], axis = 1).reset_index(drop = True)
    if "Unnamed: 0" in permuted_df.columns:
        return(permuted_df.drop("Unnamed: 0", axis = 1))
    else:
        return(permuted_df)

def average_stat(df1, df2, P, stat, stat_var = None, a = 0.95, block = "block"):
    """
    Use permutations to estimate the statistic stat using multiple imputation
    over the full data set. Return the estimate, total variance (between and
    within imputation variance), and confidence interval at the 'a' level.
    
    df1: The R data frame of the first data set.
    df2: The R data frame of the second data set. This is the data set
          to which the permutations in P will be applied.
    P: Matrix of permutations where each column is a complete permutation
          with respect to df2. The number of columns is the number of
          imputations.
    stat: The statistic to be computed. A function that accepts a data frame
          and returns a number.
    stat_var: An optional argument that is a function to compute the variance
          of the statistic defined by stat. If no function is specified, then the
          value for variance that will be returned is the sample variance of the
          estimates for stat (the between imputation variance). If a function is
          specified, then the value for variance that is returned is the total
          variance computed according to Rubin's rules for multiple imputation,
          where stat_var is the within imputation variance.
    a: Confidence level for the confidence interval.
    block: Name of the block column. The block column is removed.
    """
    if not 0 < a < 1:
        raise ValueError("The alpha value must be between 0 and 1.")
    if stat is not None and stat.__code__.co_argcount != 1:
        raise ValueError("The stat function must have a single argument")
    if stat_var is not None and stat.__code__.co_argcount != 1:
        raise ValueError("The stat function must have a single argument")
    if block in df1.columns:
        df1 = df1.drop(block, axis=1)
    if block in df2.columns:
        df2 = df2.drop(block, axis=1)
    
    if stat_var is None:
        #No within-imputation variance for 'stat'
        var_mult = 1
        stat_var = lambda x: 0
    else:
        var_mult = 1 + (1/P.shape[1])
    
    values = [0 for _ in range(0, P.shape[1])]
    stderrs = [0 for _ in range(0, P.shape[1])]
    for i in range(0, P.shape[1]):
        p = P.iloc[:,i]
        #Unshuffle df2 to link data sets
        df_i = apply_permutation(df1, df2, p)
        values[i] = stat(df_i)
        stderrs[i] = stat_var(df_i)
        
    #Total variance
    total_var = (var_mult * np.var(values)) + np.mean(stderrs)
    value_estimate = np.mean(values)
    Z = norm.ppf(a + ((1-a)/2))
    hi = value_estimate + (Z * np.sqrt(total_var))
    lo = value_estimate - (Z * np.sqrt(total_var))
    return({"estimate": value_estimate, "total_variance": total_var, "interval": [lo, hi]})
    
def switch_permutation(P):
    """
    Switch the direction of the permutation to be in terms of the data set. The
    permute_inputs function returns a permutation in terms of the second data set
    with respect to the first data set. This function will change the permutation
    to be in terms of the first data set with respect to the second.
    
    P: Dataframe/matrix of permutations as columns.
    """
    new_P = pd.DataFrame(P)
    for j in range(0, P.shape[1]):
        for i in range(0, P.shape[0]):
            val = P.iloc[i, j]
            new_P = new_P.iloc[val, j] = i
    return(new_P)
