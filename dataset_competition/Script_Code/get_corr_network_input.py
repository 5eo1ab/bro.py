# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:28:39 2017

@author: 5eo1ab
"""

import pandas as pd
from pandas import DataFrame as df
import numpy as np

## Load corr. data
import json
fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
dic_t_cols = json.load(open(fpath+'colnames.json'))
dic_n_idx = json.load(open(fpath+'nationals.json'))
nationals = list(dic_n_idx.keys())

fpath += 'EXPORTED_CSV/'
dic_n_corr = {}
for n in nationals :
    dic_n_corr[n] = pd.read_csv(fpath+"{}.csv".format("corr_{}".format(n)))
    print(n)
#dic_n_corr[nationals[0]].head()

def df_c12_counts(df_, w) :
    res = len(df_[df_['c0']==w])
    res += len(df_[df_['c1']==w])
    return res

############################
## Get input format of Gephi
############################
cutoff = 0.7
dic_nodes, dic_edges = {}, {}
for n in nationals :
    cols = list(dic_n_corr[n].columns.values)
    tmp_df = dic_n_corr[n][dic_n_corr[n]['p-value']<0.05]
    #tmp_df = dic_n_corr[n][dic_n_corr[n]['p-value']<0.05][dic_n_corr[n]['corr']>cutoff]
    
    nodes = [dic_n_idx[n]] + list(dic_t_cols[n][1:])
    node_df = df({ 
        'count' : [df_c12_counts(tmp_df ,w) for w in nodes],
        'id' : ['n{}'.format(i) for i in range(len(nodes))],
        'label' : nodes
        })
    dic_label = {k:v for v,k in zip(node_df['id'], node_df['label'])}
    edge_df = df({
        'source' : tmp_df['c0'].map(dic_label), 
        'target' : tmp_df['c1'].map(dic_label),
        'weight' : np.abs(tmp_df['corr'])
        })
    edge_df['type'] = 'undirected'
    dic_nodes[n], dic_edges[n] = node_df, edge_df
    print(n)

## Export to CSV format
for n in nationals :
    dic_nodes[n].to_csv(fpath+"gephi_{}_node.csv".format(n), index=False)
    dic_edges[n].to_csv(fpath+"gephi_{}_edge.csv".format(n), index=False)

