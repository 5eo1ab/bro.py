# -*- coding: utf-8 -*-
"""
Created on Mon May 22 23:34:16 2017

@author: SERVER1
"""

###########################
# >> Run get_dic_t_df.py
###########################
dic_t_df.keys()
dic_t_cols.keys()
dic_n_idx.keys()

###########################
# Read diff. Table
###########################\
fpath
y_bin = pd.read_csv(fpath+"Y_IDX_CLOSE.csv")

dic_n_diff_df = {} # t lag, diff table
dic_n_y_arr = {}
dic_n_bin_arr = {}
for n in nationals:
    dic_n_diff_df[n] = pd.read_csv(fpath+"Input_CSV/diff_{}.csv".format(n))
    tl_cutoff = len(dic_n_diff_df[n])
    dic_n_y_arr[n] = dic_t_df['G_IDX_CLOSE'][dic_n_idx[n]][-tl_cutoff:]
    dic_n_y_arr[n] = dic_n_y_arr[n].reset_index(drop=True)
    dic_n_bin_arr[n] = y_bin[dic_n_idx[n]][-tl_cutoff:]
    dic_n_bin_arr[n] = dic_n_bin_arr[n].reset_index(drop=True)

###########################
# l1 penalty variable selection
###########################
from sklearn.linear_model import LogisticRegression
dic_n_cols_l1 = {} # selected by logistic regression l1 penalty
for n in nationals :
    X = dic_n_diff_df[n][:-48]
    y = dic_n_bin_arr[n][:-48]
    # C 값을 조정하여 coefficient값이 0인 변수 수를 조절 할 수 있음
    model = LogisticRegression(penalty='l1',C=0.1)
    model.fit(X,y)
    cols = X.columns.values[np.where(model.coef_ != 0)[1]]
    dic_n_cols_l1[n] = cols
###########################
# Random Forest variable selection
###########################    
from sklearn.ensemble import RandomForestClassifier
dic_n_cols_rf = {} # selected by random forest
for n in nationals :
    X = dic_n_diff_df[n][:-48]
    y = dic_n_bin_arr[n][:-48]
    model = RandomForestClassifier()
    model.fit(X,y)
    cols = X.columns.values[np.where(model.feature_importances_ != 0)[0]]
    dic_n_cols_rf[n] = cols

dic_union = {}
dic_intersection = {}
for n in nationals :
    dic_union[n] = set(dic_n_cols_l1[n]) | set(dic_n_cols_rf[n])
    dic_intersection[n] = set(dic_n_cols_l1[n]) & set(dic_n_cols_rf[n])

fpath    
var_counts = []
for n in nationals :
    var_counts.append([ n,
            len(dic_n_diff_df[n].columns.values),
            len(dic_n_cols_l1[n]),
            len(dic_n_cols_rf[n]),
            len(dic_union[n]),
            len(dic_intersection[n])
            ])
    print("{}\tunion: {}\tintersection:{}".format(
            n, len(dic_union[n]), len(dic_intersection[n])))
var_counts = df(var_counts, columns=[
            'national', 'corr', 'l1', 'RF', 'union', 'intersection'])
var_counts.to_csv(fpath+"var_counts.csv", index=False)

