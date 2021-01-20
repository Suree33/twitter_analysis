import pandas as pd
import graph_tool.all as gt

# 処理するユーザー名
user_name = 'goando'

g = gt.Graph()
center = g.add_vertex()


df_RT = pd.read_csv('data/connected.' + user_name + '.csv')

for index, row in df_RT.iterrows():
    if row['follower'] == 1:
        v = g.add_vertex()
        g.add_edge(v, center)
    elif row['follower'] == 0:
        v = g.add_vertex()

gt.graph_draw(g,
              # vertex_text=g.vertex_index,
              vertex_fill_color="#fafafa",
              output="img/graph/graph" + user_name + ".png"
              )
