# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:42:57 2017

@author: 5eo1ab
"""



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

#df_in = dic_t_df['G_IDX_CLOSE']
#df_out = get_modeling_input(df_in, t=1)


