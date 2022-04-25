import igraph

def get_label(ind, Q, M, N):
    z = ind // ((M + 1) * (Q + 1))
    x = (ind % ((M + 1) * (Q + 1))) // (M + 1)
    y = (ind % ((M + 1) * (Q + 1))) % (M + 1)

    return (x, y, z)

def get_edge_label(lst, symbol_info):
    ALPHA = symbol_info.ALPHA
    ALPHA_C = symbol_info.ALPHA_C
    BETA = symbol_info.BETA
    BETA_C = symbol_info.BETA_C
    POLICY = symbol_info.POLICY

    symbol_mapper = {}
    symbol_mapper[ALPHA] = 'α'
    symbol_mapper[ALPHA_C] = '(1.0 - α)'
    symbol_mapper[BETA] = 'β'
    symbol_mapper[BETA_C] = '(1.0 - β)'

    for i in range(len(POLICY)):
        symbol_mapper[POLICY[i]] = '(g{})'.format(i)

    return ".".join([symbol_mapper[x] for x in lst])

class MDPVisualizer:

    def __init__(self, N, M, Q, adj_list, symbol_info) -> None:
        self.N = N
        self.M = M
        self.Q = Q
        self.adj_list = adj_list
        self.symbol_info = symbol_info

    def draw(self):
        # defs
        Q = self.Q
        N = self.N
        M = self.M

        g = igraph.Graph()
        vs = {}
        vs["margin"] = 100


        cnt = N * (M + 1) * (Q + 1)
        g.add_vertices(cnt)

        g.vs["label"] = [get_label(i, Q, M, N) for i in range(cnt)]
        mapper = {}
        for i in range(cnt):
            mapper[get_label(i, Q, M, N)] = i

        layout = g.layout_grid(width=(cnt) // N)
        edge_labels = []

        for key in self.adj_list:
            for transition in self.adj_list[key]:
                print('trans', transition)
                v = transition[1]
                g.add_edges([(mapper[key], mapper[v])])
                edge_labels.append(get_edge_label(transition[0], symbol_info=self.symbol_info))

        vs["bbox"] = (4000, 4000)
        g.es["label"] = edge_labels
        vs["vertex_size"] = 30
        print(layout)
        igraph.plot(g, layout=layout, **vs)

from mdp_creator import MDPCreator
from symbol import SymbolInfo

symbol_info = SymbolInfo(4)
mdp = MDPCreator(N = 2, M = 2, Q = 3, symbol_info=symbol_info).create()

vis = MDPVisualizer(N = 2, M = 2, Q = 3, adj_list = mdp, symbol_info=symbol_info)

vis.draw()