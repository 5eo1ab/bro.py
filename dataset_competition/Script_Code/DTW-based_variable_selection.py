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

def get_norm_tg_arr(arr) :
    arr = (arr - arr.min()) / (arr.max() - arr.min())
    arr = arr.reset_index(drop=True)
    return arr



def get_norm_df(df_) :
    arr_tl = df_['TimeLog']
    cols = [c for c in list(df_.columns.values) if c!='TimeLog']
    df_ = df_[cols]
    df_norm = (df_ - df_.min()) / (df_.max() - df_.min())
    df_norm['TimeLog'] = arr_tl
    df_norm = df_norm[['TimeLog']+cols]
    return df_norm
           

############################
## Get DTW(Dynamic Time Warping) 
############################
"""
n, t = nationals[0], 1
df_n = df_n_merged[n]
g_idx = dic_t_df['G_IDX_CLOSE'][dic_n_idx[n]][:len(df_n)]

df_n = get_lag_norm_df(df_n, t)
g_idx = get_norm_tg_arr(g_idx)
cutoff = get_cutoff_DTW(g_idx, t)

cols = df_n.columns.values
v_li = []
for c in cols:
    dtw, _ = fastdtw(g_idx, df_n[c])
    if dtw < cutoff :
        v_li.append([c, dtw])
print(len(v_li), len(cols))
"""

n = nationals[0]
df_n = df_n_merged[n]
g_idx = dic_t_df['G_IDX_CLOSE'][dic_n_idx[n]]

g_idx_n = (g_idx - g_idx.min()) / (g_idx.max() - g_idx.min())
df_n = get_norm_df(df_n)

cols = df_n.columns.values
v_li = []
for c in cols[1:]:
    dtw, _ = fastdtw(g_idx_n, df_n[c])
    v_li.append([c, dtw])
print(len(v_li), len(cols))

df_tmp = df(v_li, columns=['index', 'DTW'])


