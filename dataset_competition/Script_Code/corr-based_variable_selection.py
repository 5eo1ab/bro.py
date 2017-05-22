# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:27:50 2017

@author: 5eo1ab
"""

###########################
# >> Run get_dic_t_df.py
###########################
dic_t_df.keys()
dic_t_cols.keys()
dic_n_idx.keys()

###########################
# Read Merged Table
###########################
fpath = "C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/"

dic_n_df = {}
for n in nationals:
    dic_n_df[n] = pd.read_csv(fpath+"MERGED_{}.csv".format(n))

dic_n_g_idx = {}
for n in nationals:
    dic_n_g_idx[n] = dic_t_df['G_IDX_CLOSE'][['TimeLog',  dic_n_idx[n]]]

###########################
# Functions
###########################
"""
def lag_table(df_, t) :
    d_range = [-t+i for i in range(t)] if t!=1 else -1
    df_ = df_.drop(df_.index[d_range], axis=0)
    min_tl = df_['TimeLog'].min()
    del df_['TimeLog']
    return df_, min_tl

def lag_target_arr(df_tg, min_tl, t) :
    df_tg = df_tg[df_tg['TimeLog']>=tl]
    d_range = [i for i in range(t)] if t!=1 else 0
    df_tg = df_tg.drop(df_tg.index[d_range], axis=0)
    df_tg = df_tg.reset_index(drop=True)
    return df_tg[df_tg.columns.values[-1]]
"""

# >> Run get_modeling_input.py
def get_modeling_input(df_in, t=1) :
    cols = [c for c in list(df_in.columns.values) if c!='TimeLog']
    df_out = df({'TimeLog': list(df_in['TimeLog'][t:])})
    for t0 in range(1,t+1) :
        cols_t = ["{}_{}".format(c,t0) for c in cols]
        d_range = [-t+i+(t0-1) for i in range(t)] if t!=1 else -1
        df_tmp = df(
                df_in.drop(df_in.index[d_range], axis=0)[cols].values,
                columns=cols_t)
        for c_t in cols_t :
            df_out[c_t] = df_tmp[c_t].values
        pass   
    return df_out

df_in = dic_n_t_df[n]
def get_diff_df(df_in) :
    diff_df = []
    arr_tl = df_in['TimeLog'][1:]
    df_in = df_in[list(df_in.columns.values)[1:]]
    for i in range(1, len(df_in)):
        row = (np.array(df_in[df_in.index==i]) - np.array(df_in[df_in.index==i-1]))
        row = row/(np.array(df_in[df_in.index==i-1]))*100
        row = [0 if np.isinf(row)[0][j] else row[0][j] for j in range(len(row[0]))]
        diff_df.append([arr_tl[i]]+row)
    df_out = df(diff_df, columns=['TimeLog'] + list(df_in.columns.values))
    return df_out



###########################
###########################
dic_n_t_df = {} # t lag append table
for n in nationals:
    dic_n_t_df[n] = get_modeling_input(dic_n_df[n], t=3)

from scipy.stats import pearsonr
dic_n_corr_df = {} # variable selection by corr.
cutoff = 0.3
for n in nationals:
    corr_li, tl = [], dic_n_t_df[n]['TimeLog'].min()
    tg_arr = dic_n_g_idx[n][dic_n_g_idx[n]['TimeLog']>=tl][dic_n_idx[n]]    
    tg_arr = tg_arr.reset_index(drop=True)
    for c in dic_n_t_df[n].columns.values[1:]:
        corr, p_v = pearsonr(tg_arr, dic_n_t_df[n][c])
        if p_v < 0.05 and abs(corr) > cutoff:
            corr_li.append(c)
    dic_n_corr_df[n] = dic_n_t_df[n][corr_li]

fpath = '/'.join(fpath.split('/')[:-2])+'/Input_CSV/'
for n in nationals:
    dic_n_corr_df[n].to_csv(fpath+"corr_{}.csv".format(n), index=False)


dic_n_diff_df = {} # t lag, diff table
for n in nationals:
    cols = list(dic_n_corr_df[n].columns.values)
    dic_n_diff_df[n] = get_diff_df(dic_n_t_df[n])[cols]
fpath = '/'.join(fpath.split('/')[:-2])+'/Input_CSV/'
for n in nationals:
    dic_n_diff_df[n].to_csv(fpath+"diff_{}.csv".format(n), index=False)

