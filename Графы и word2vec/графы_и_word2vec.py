# -*- coding: utf-8 -*-

!pip install networkx

!pip install gensim

import networkx as nx
import matplotlib.pyplot as plt 
import sys
import gensim, logging
import urllib.request

urllib.request.urlretrieve("http://rusvectores.org/static/models/rusvectores2/ruscorpora_mystem_cbow_300_2_2015.bin.gz", "ruscorpora_mystem_cbow_300_2_2015.bin.gz")

m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)

model.init_sims (replace=True)

verbs = ['бежать_VERB', 'идти_VERB', 'ускоряться_VERB', '_VERB', 'перемещаться_VERB', 'двигаться_VERB', 'шагать_VERB', 'нестись_VERB', 'лететь_VERB', 'скакать_VERB', 'ехать_VERB']

G = nx.Graph()
G.add_nodes_from(verbs)
for word in verbs:
  if word in model:
    Cos = model.similarity(word, word)
    if Cos < 0.9999 and Cos > 0.5:
       G.add_edge(word, word)
   else:
     print('There is no such word in model')
print('узлы', G.nodes())
print('рёбра', G,edges())

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(dolphin_G, pos, node_color='black', node_size=25) 
nx.draw_networkx_edges(dolphin_G, pos, edge_color='red')
nx.draw_networkx_labels(dolphin_G, pos, font_size=10, font_family='Arial')
plt.axis('off') 
plt.show()

central_words = []
deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
  central_words.append(nedeid)
print('Центральные слова в графе:', ", ".join(central_words[:3]))

print('Радиус графа:', nx.redius(G))

print('Коэффициент кластеризации:', nx.average_clustering(G))
