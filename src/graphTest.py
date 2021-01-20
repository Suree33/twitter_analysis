import graph_tool.all as gt

g = gt.Graph()

v1 = g.add_vertex()
v2 = g.add_vertex()

e = g.add_edge(v1, v2)

gt.graph_draw(g, vertex_text=g.vertex_index, output="two-nodes.png")
