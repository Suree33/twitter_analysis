import csv
from os import close
import graph_tool.all as gt
import pandas as pd

# 処理するユーザー名
user_name = 'goando'

nodes = set()
rows = []

df_RT = pd.read_csv('connected.'+user_name+'.csv')
RT_ids = df_RT.values.to_dict()

for id in RT_ids:
    if id['follower'] == 1:
