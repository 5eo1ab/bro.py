# -*- coding: utf-8 -*-
"""
Created on Sun May 21 21:27:34 2017

@author: 5eo1ab
"""

###########################
# >> Run get_dic_t_df.py
###########################
dic_t_df.keys()
dic_t_cols.keys()
dic_n_idx.keys()

###########################
# import MERGED_N TABLE
###########################
fpath = "C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/"
df_n_merged = {}
for n in nationals:
    df_n_merged[n] = pd.read_csv(fpath+"MERGED_{}.csv".format(n))

###########################
# function
###########################

from fastdtw import fastdtw
def get_cutoff_DTW(arr, t) :
    dtw, _ = fastdtw(arr[:t], arr[t:])
    return dtw

def get_lag_norm_df(df_, t) :
    cols = [c for c in list(df_.columns.values) if c!='TimeLog']
    r_idx = [-t+i for i in range(t)] if t!=1 else -t
    df_ = df_.drop(df_.index[r_idx], axis=0)[cols]
    df_.reset_index(drop=True)
    df_norm = (df_ - df_.min()) / (df_.max() - df_.min())
    return df_norm

def get_norm_tg_arr(arr, t) :
    arr = (arr - arr.min()) / (arr.max() - arr.min())
    arr = arr.reset_index(drop=True)
    return arr

############################
## Get DTW(Dynamic Time Warping) 
############################
df_n_merged[n].head()

