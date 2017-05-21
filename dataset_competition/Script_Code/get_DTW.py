# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:46:51 2017

@author: 5eo1ab
"""



############################
## Get DTW(Dynamic Time Warping) 
############################

def has_missing(ar) :
    if False in list(ar[:2]==pd.Series([0,0])) :
        return False
    return True
def get_idx_missing(ar) :
    if has_missing(ar) is False :
        return 0
    return ar[ar>0].index[0]-1

fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
dic_n_idx = json.load(open(fpath+'nationals.json'))
nationals = list(dic_n_idx.keys())

from fastdtw import fastdtw
dic_n_dtw = {}
for n in nationals :
    cols = list(dic_t_df[n].columns.values)[1:]
    g_index = dic_t_df['G_IDX_CLOSE'][dic_n_idx[n]]
    g_index = (g_index - g_index.min()) / (g_index.max() - g_index.min())
    res_li = []
    tmp_n_df = dic_t_df[n][
            dic_t_df[n]['TimeLog']>=dic_t_df['G_IDX_CLOSE']['TimeLog'][0]]
    tmp_n_df = tmp_n_df.drop(['TimeLog'], axis=1)
    tmp_n_df = (tmp_n_df - tmp_n_df.min()) / (tmp_n_df.max() - tmp_n_df.min())
    tmp_n_df = tmp_n_df.reset_index(drop=True)
    for c0 in cols :
        s_idx = get_idx_missing(tmp_n_df[c0])
        dtw, _ = fastdtw(g_index[s_idx:], tmp_n_df[c0][s_idx:])
        res_li.append([dic_n_idx[n], c0, dtw])
    for c0 in cols[:-1] :
        c0_idx = get_idx_missing(dic_t_df[n][c0])
        for c1 in cols[cols.index(c0)+1:] :
            #print(c0,c1)
            tmp_li = [c0, c1]
            if c0_idx > get_idx_missing(dic_t_df[n][c1]):
                s_idx = get_idx_missing(dic_t_df[n][c1])
            else :
                s_idx = c0_idx
            dtw, _ = fastdtw(g_index[s_idx:], tmp_n_df[c0][s_idx:])
            res_li.append([dic_n_idx[n], c0, dtw])
    dic_n_dtw[n] = df(res_li, columns=['c0', 'c1', 'DTW'])
    print(n)

ex_dir = 'C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/'
for n in nationals :
    dic_n_dtw[n].to_csv(ex_dir+"{}.csv".format("DTW_{}".format(n)), index=False)
    