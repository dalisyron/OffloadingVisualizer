from symbol import SymbolInfo


def phi(z):
    return max(z - 1, 0)


class MDPCreator:

    def __init__(self, Q: int, M: int, N: int, symbol_info: SymbolInfo) -> None:
        self.Q = Q
        self.M = M
        self.N = N
        self.symbol_info = symbol_info

    def get_policy_candidates(self, state):
        q, m, n = state
        assert(q >= 0)

        res = [0]

        if q >= 1:
            if (m == 0):
                res.append(2)
            if (n == 0):
                res.append(1)

        if q >= 2:
            if (m == 0 and n == 0):
                res.append(3)

        return res

    # state: x, y, z
    # w/ x < Q
    def get_outcomes_for_policy(self, state, p):
        x, y, z = state
        assert(0 <= x < self.Q)

        # defs
        POLICY = self.symbol_info.POLICY
        BETA = self.symbol_info.BETA
        BETA_C = self.symbol_info.BETA_C
        N = self.N
        M = self.M

        if p == 0:
            if y == 0:
                return [
                    (
                        [POLICY[0]],
                        (x, y, phi(z))
                    )
                ]
            else:
                return [
                    (
                        [POLICY[0], BETA],
                        (x, y - 1, phi(z))
                    ),
                    (
                        [POLICY[0], BETA_C],
                        (x, y, phi(z))
                    )
                ]
        elif p == 1:
            assert(z == 0 and x > 0)
            if y == 0:
                return [
                    (
                        [POLICY[1]],
                        (x - 1, 0, N - 1)
                    )
                ]
            else:
                return [
                    (
                        [POLICY[1], BETA],
                        (x - 1, y - 1, N - 1)
                    ),
                    (
                        [POLICY[1], BETA_C],
                        (x - 1, y, N - 1)
                    )
                ]
        elif p == 2:
            assert(y == 0 and x > 0)
            return [
                (
                    [POLICY[2], BETA],
                    (x - 1, M - 1, phi(z))
                ),
                (
                    [POLICY[2], BETA_C],
                    (x - 1, M, phi(z))
                )
            ]
        elif p == 3:
            assert(x > 1 and y == 0 and z == 0)
            return [
                (
                    [POLICY[3], BETA],
                    (x - 2, M - 1, N - 1)
                ),
                (
                    [POLICY[3], BETA_C],
                    (x - 2, M, N - 1)
                )
            ]
        
        print('policy', p)

    def get_transitions(self, state):
        # defs
        ALPHA = self.symbol_info.ALPHA
        ALPHA_C = self.symbol_info.ALPHA_C
        POLICY = self.symbol_info.POLICY

        if state[0] == self.Q:
            return [([POLICY[0]], (0, 0, 0))]

        policies = self.get_policy_candidates(state)
        transitions = []

        for p in policies:
            states = self.get_outcomes_for_policy(state, p)
            for s in states:
                x, y, z = s[1]
                transitions.append(([ALPHA] + s[0], (x + 1, y, z)))
                transitions.append(([ALPHA_C] + s[0], (x, y, z)))

        return transitions

    def format_symbols(self, adj_list):
        for key in adj_list:
            for transition in adj_list[key]:
                transition[0].sort()

    def create(self):
        # defs
        Q = self.Q
        M = self.M
        N = self.N
        adj_list = {}

        for i in range(Q + 1):
            for j in range(M + 1):
                for k in range(N):
                    adj_list[(i, j, k)] = []

        for i in range(Q + 1):
            for j in range(M + 1):
                for k in range(N):
                    transitions = self.get_transitions((i, j, k))

                    for t in transitions:
                        adj_list[(i, j, k)].append(t)

        # self.format_symbols(adj_list)
        
        return adj_list