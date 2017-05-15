# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:28:39 2017

@author: 5eo1ab
"""

import pandas as pd
from pandas import DataFrame as df
import numpy as np

## Load corr. data
nationals = ['KR_INDEX', 'US_INDEX', 'CN_INDEX', 'JP_INDEX', 'DE_INDEX']
im_dir = 'C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/'
dic_n_corr = {}
for n in nationals :
    dic_n_corr[n] = pd.read_csv(im_dir+"{}.csv".format("corr_{}".format(n)))
#dic_n_corr[nationals[0]].head()

import json
fpath = r'C:\Users\SERVER1\bro.py\dataset_competition\colnames.json'
dic_t_cols = json.load(open(fpath))

cols = list(dic_n_corr[n].columns.values)
tmp_df = dic_n_corr[n]
cutoff = 0.7
tmp_df2 = tmp_df[tmp_df['p-value']<0.05][abs(tmp_df['corr'])>cutoff]


def df_c12_counts(df_, w) :
    res = len(df_[df_['c0']==w])
    res += len(df_[df_['c1']==w])
    return res

ids = ['n{}'.format(i) for i in range(len(dic_t_cols[n][1:]))]
counts = [df_c12_counts(tmp_df2 ,w) for w in dic_t_cols[n][1:]]
node_df = df({ 
        'count' : [df_c12_counts(tmp_df2 ,w) for w in dic_t_cols[n][1:]],
        'id' : ['n{}'.format(i) for i in range(len(dic_t_cols[n][1:]))],
        'label' : dic_t_cols[n][1:]
        })
tmp_dic = {k:v for v,k in zip(node_df['id'], node_df['label'])} 
edge_df = df({
        'source' : tmp_df2['c0'].map(tmp_dic), 
        'target' : tmp_df2['c1'].map(tmp_dic),
        'weight' : tmp_df2['corr'], 
        'type' : 'undirected'
        })

im_dir    
node_df.to_csv(im_dir+"TMP_node.csv", index=False)
edge_df.to_csv(im_dir+"TMP_edge.csv", index=False)
    
    



    
dic_t_cols[n][23]
len(tmp_df2[tmp_df2['c0']=="aGLIRPCEU"])+len(tmp_df2[tmp_df2['c1']=="aGLIRPCEU"])

zip(node_df['id'], node_df['label'])
node_df[['id', 'label']]



nodes = 
len(set(tmp_df2['c0']))
len(set(tmp_df2['c1']))
len(np.setdiff1d(set(tmp_df2['c1']), set(tmp_df2['c0']))[0])

edge_df = df({'source' : tmp_df2['c0'], 
              'target' : tmp_df2['c1'],
              'weight' : tmp_df2['corr'], 
              'type' : 'undirected'
        })
