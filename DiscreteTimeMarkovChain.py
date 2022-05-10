
class DiscreteTimeMarkovChain:

    def __init__(self, N: int, M: int, Q: int, adj_list: dict) -> None:
        self.N = N
        self.M = M
        self.Q = Q
        self.adj_list = adj_list