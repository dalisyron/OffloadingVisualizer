def phi(z):
    return max(0, z - 1)

def edgize(source, dests):
    res = []
    for d in dests:
        res.append((source, d))
    return res

class FormulaEdgeGenerator:

    def __init__(self, Q, M, N):
        self.Q = Q
        self.M = M
        self.N = N

    def case1_edges(self, state):
        x, y, z = state
        res = [(1, 0, phi(z)), (0, 0, phi(z))]

        return edgize(state, res)

    def case2_edges(self, state):
        x, y, z = state

        res = []
        res.append((1, phi(y), phi(z)))
        res.append((1, y, phi(z)))
        res.append((0, phi(y), phi(z)))
        res.append((0, y, phi(z)))
        return edgize(state, res)


    def case3_edges(self, state):
        res = []
        res.append((1, 0, 0))
        res.append((0, 0, self.N - 1))
        res.append((0, self.M - 1, 0))
        res.append((0, self.M, 0))
        res.append((2, 0, 0))
        res.append((1, 0, self.N - 1))
        res.append((1, self.M - 1, 0))
        res.append((1, self.M, 0))

        return edgize(state, res)


    def case4_edges(self, state):
        x, y, z = state
        res = []

        res.append((x, 0, phi(z)))
        res.append((x - 1, self.M - 1, phi(z)))
        res.append((x - 1, self.M, phi(z)))
        res.append((x + 1, 0, phi(z)))
        res.append((x, self.M - 1, phi(z)))
        res.append((x, self.M, phi(z)))
        return edgize(state, res)


    def case5_edges(self, state):
        x, y, z = state
        res = []

        res.append((x, y, 0))
        res.append((x, phi(y), 0))
        res.append((x - 1, y, self.N - 1))
        res.append((x - 1, phi(y), self.N - 1))
        res.append((x + 1, y, 0))
        res.append((x + 1, phi(y), 0))
        res.append((x, y, self.N - 1))
        res.append((x, phi(y), self.N - 1))

        return edgize(state, res)


    def case6_edges(self, state):
        x, y, z = state
        res = []

        res.append((x + 1, phi(y), phi(z)))
        res.append((x + 1, y, phi(z)))
        res.append((x, phi(y), phi(z)))
        res.append((x, y, phi(z)))

        return edgize(state, res)

    def case7_edges(self, state):
        x, y, z = state
        res = []

        res.append((x, 0, 0))
        res.append((x - 1, 0, self.N - 1))
        res.append((x - 1, self.M, 0))
        res.append((x - 1, self.M - 1, 0) )
        res.append((x - 2, self.M, self.N - 1))
        res.append((x - 2, self.M - 1, self.N - 1))
        res.append((x + 1, 0, 0))
        res.append((x, 0, self.N - 1))
        res.append((x, self.M, 0))
        res.append((x, self.M - 1, 0) )
        res.append((x - 1, self.M, self.N - 1))
        res.append((x - 1, self.M - 1, self.N - 1))

        return edgize(state, res)

    def case8_edges(self, state):
        return edgize(state, [(0, 0, 0)])

    def case9_edges(self, state):
        x, y, z = state
        res = []

        res.append((0, y, 0))
        res.append((0,y - 1, 0))
        res.append((1, y, 0))
        res.append((1, y - 1, 0))

        return edgize(state, res)

    def get_edges_based_on_formula(self):
        edges = []

        # Case 1
        for z in range(self.N):
            edges += self.case1_edges((0, 0, z))

        # Case 2
        for y in range(1, self.M + 1):
            for z in range(1, self.N):
                edges += self.case2_edges((0, y, z))

        # Case 3
        edges += self.case3_edges((1, 0, 0))

        # Case 4
        for x in range(1, self.Q):
            for z in range(1, self.N):
                edges += self.case4_edges((x, 0, z))

        # Case 5
        for x in range(1, self.Q):
            for y in range(1, self.M + 1):
                edges += self.case5_edges((x, y, 0))

        # Case 6
        for x in range(1, self.Q):
            for y in range(1, self.M + 1):
                for z in range(1, self.N):
                    edges += self.case6_edges((x, y, z))

        # Case 7
        for x in range(2, self.Q):
            edges += self.case7_edges((x, 0, 0))

        # Case 8
        for y in range(self.M + 1):
            for z in range(self.N):
                edges += self.case8_edges((self.Q, y, z))

        # Case 9
        for y in range(1, self.M + 1):
            edges += self.case9_edges((0, y, 0))
        
        return edges

feg = FormulaEdgeGenerator(Q=500, M=10, N=20)
edges = feg.get_edges_based_on_formula()
print(len(edges))