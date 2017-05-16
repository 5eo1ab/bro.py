# -*- coding: utf-8 -*-
"""
Created on Mon May 15 22:48:59 2017

@author: 5eo1ab
"""

import json
nationals = {'KR_INDEX':'KOSPI', 'US_INDEX':'SPX', 'CN_INDEX':'SSEC', 
             'JP_INDEX':'N225', 'DE_INDEX':'GDAXI'}

fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
with open(fpath+'nationals.json', 'w') as fp :
    json.dump(nationals, fp)



