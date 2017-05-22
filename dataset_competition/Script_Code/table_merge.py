# -*- coding: utf-8 -*-
"""
Created on Sun May 21 19:17:02 2017

@author: 5eo1ab
"""

###########################
# >> Run get_dic_t_df.py
###########################
dic_t_df.keys()
dic_t_cols.keys()
dic_n_idx.keys()

def get_re_colnames(df_, tag) :
    res = ["{}_{}".format(c,tag)  if c != 'TimeLog' else 'TimeLog'
            for c in df_.columns.values]
    return res

def table_merge(df_l, df_r) :
    tl_cutoff = [d['TimeLog'].min() for d in [df_l, df_r]]
    tl_cutoff = max(tl_cutoff)
    
    df_l = df_l[df_l['TimeLog']>=tl_cutoff]
    df_r = df_r[df_r['TimeLog']>=tl_cutoff]
    df_l = df_l.reset_index(drop=True)
    df_r = df_r.reset_index(drop=True)

    df_res = df_l.merge(df_r, on='TimeLog')
    return df_res







###########################
# >> Script
###########################

### Global index
df_list = [dic_t_df[g] for g in ['G_IDX_CLOSE', 'G_IDX_VOLUME', 
           'G_IDX_M_CAPITAL', 'G_IDX_EPS', 'G_IDX_PER']]
for i in range(len(df_list)):
    df_list[i].columns = get_re_colnames(df_list[i], g_idxes[i].split('_')[-1])
df_g_idx = df_list[0].copy()
for i in range(1, len(df_list)):
    df_g_idx = table_merge(df_g_idx, df_list[i])

fpath = "C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/"
df_g_idx.to_csv(fpath+"MERGED_G_IDX.csv", index=False)


### Primary index
df_list = [ dic_t_df[i]
        for i in ['NORMAL_IDX', 'MATERIALS', 'EXCHANGES', 'OTHER_IDX']]
df_p_idx = df_list[0].copy()
for i in range(1, len(df_list)):
    df_p_idx = table_merge(df_p_idx, df_list[i])

fpath = "C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/"
df_p_idx.to_csv(fpath+"MERGED_P_IDX.csv", index=False)

### append national index
df_n_merged = {}
for n in nationals:
    df_n_merged[n] = dic_t_df[n].copy()
    df_n_merged[n] = table_merge(df_n_merged[n], df_g_idx)
    df_n_merged[n] = table_merge(df_n_merged[n], df_p_idx)

fpath = "C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/"
for n in nationals:
    df_n_merged[n].to_csv(fpath+"MERGED_{}.csv".format(n), index=False)
