import graphviz as gv
from DiscreteTimeMarkovChain import DiscreteTimeMarkovChain
import symbol
from random import choice
from colors import rgb_colors

class GridGraphRenderer:

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

    def index_from_position(self, r, c):
        return r * self.width + c

    def name_from_position(self, r, c):
        return str(r * self.width + c)

    def set_node_labels_matrix(self, node_labels_matrix):
        self.node_labels_matrix = node_labels_matrix

    def has_edges(self):
        return self.edges != None and type(self.edges) == list and len(self.edges) > 0

    def dot_output(self):
        dot = gv.Digraph()
        dot.graph_attr['label'] = 'Markov Chain for Task Offloading'
        dot.graph_attr['labelloc'] = 't'
        dot.graph_attr['margin'] = '5'

        dot.node_attr['shape'] = 'circle'
        dot.node_attr['width'] = '1'
        dot.node_attr['fixedsize'] = 'true'
        dot.node_attr['fontsize'] = '12'
        dot.graph_attr['splines'] = 'false'

        nfp = self.name_from_position

        for r in range(self.height):
            row_graph = gv.Digraph('row{}'.format(r))
            row_graph.edge_attr['style'] = 'invis'
            row_graph.edge_attr['weight'] = '1000'
            row_graph.edge_attr['minlen'] = '25'


            row_graph.attr(rank = 'same')
            for c in range(self.width):
                id = str(r * self.width + c)
                
                if self.node_labels_matrix != None:
                    label = self.node_labels_matrix[r][c]
                    row_graph.node(id, label)
                else:
                    row_graph.node(id, "({},{})".format(r, c))

            for c in range(self.width - 1):
                row_graph.edge(nfp(r, c), nfp(r, c + 1))

            dot.subgraph(row_graph)
            

        grid = gv.Digraph('subgraph_grid')
        grid.edge_attr['style'] = 'invis'
        grid.edge_attr['minlen'] = '25'
        grid.edge_attr['weight'] = '1000'

        for c in range(self.width):
            for r in range(self.height - 1):
                grid.edge(nfp(r, c), nfp(r + 1, c))
        
        dot.subgraph(grid)


        if self.has_edges():
            with dot.subgraph(name='subgraph_input_edges') as sub:
                sub.edge_attr['constraint'] = 'false'

                for edge in self.edges:
                    start,end, label = edge 
                    color = color=choice(rgb_colors)
                    sub.edge("{}".format(start), "{}".format(end), color=color, label=label, fontcolor=color)

        if self.node_labels_matrix != None:
        
            dot._node

        return dot

class DTMCVisualizer:

    def __init__(self, dtmc: DiscreteTimeMarkovChain) -> None:
        self.dtmc = dtmc

    def grid_height(self):
        return self.dtmc.N

    def grid_width(self):
        M = self.dtmc.M
        Q = self.dtmc.Q

        return (M + 1) * (Q + 1)


    def get_edge_label(self, symbol_list: list):
        symbol_strings = []

        for s in symbol_list:
            if s == symbol.ALPHA:
                symbol_strings.append('α')
            elif s == symbol.ALPHA_C:
                symbol_strings.append('(1.0 - α)')
            elif s == symbol.BETA:
                symbol_strings.append('β')
            elif s == symbol.BETA_C:
                symbol_strings.append('(1.0 - β)')
            elif isinstance(s, symbol.PolicySymbol):
                symbol_strings.append('(g{})'.format(s.number))

        return ".".join(symbol_strings)

    def grid_position_by_state(self, state):
        queue_count, tu_state, cpu_state = state
        M = self.dtmc.M

        row = cpu_state
        column = queue_count * (M + 1) + tu_state

        return (row, column)

    def grid_id_by_state(self, state):
        row, column = self.grid_position_by_state(state)

        return "{}".format(row * self.grid_width() + column)

    def visualize(self):
        N = self.dtmc.N
        M = self.dtmc.M
        Q = self.dtmc.Q

        height = self.grid_height()
        width = self.grid_width()

        renderer = GridGraphRenderer(height=height, width=width)

        node_labels_matrix = [] 
        for r in range(height):
            row = []
            for c in range(width):
                queue_count = c // (M + 1)
                cpu_state = r
                tu_state = c % (M + 1)
                row.append(str((queue_count, tu_state, cpu_state)))

            node_labels_matrix.append(row)

        renderer.set_node_labels_matrix(node_labels_matrix)

        edges = []
        for source, transitions in self.dtmc.adj_list.items():
            for transition in transitions:
                symbols, dest = transition
                label = self.get_edge_label(symbols)

                source_grid_id = self.grid_id_by_state(source)
                dest_grid_id = self.grid_id_by_state(dest)

                edges.append((source_grid_id, dest_grid_id, label))

        renderer.edges = edges

        graphviz = renderer.dot_output()
        return graphviz