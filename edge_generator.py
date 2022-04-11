
beta = 0.5
alpha = 0.5
M = 10
N = 20
Q = 500


def edge_count_formula(N, M, Q):
    return N * 2 + M * (N - 1) * 4 + 1 * 8 + (Q - 1) * (N - 1) * 6 + (Q - 1) * M * 8 + (Q - 1) * M * (N - 1) * 4 + (Q - 2) * 12 + (M + 1) * N * 1 + M * 4


def get_policy_candidates(state):
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


def phi(z):
    return max(0, z - 1)


def get_outcomes_for_policy(state, policy):
    x, y, z = state

    if policy == 0:
        if y == 0:
            return [(1.0, (x, y, phi(z)))]
        else:
            return [(beta, (x, y - 1, phi(z))), (1.0 - beta, (x, y, phi(z)))]
    elif policy == 1:
        assert(z == 0 and x > 0)
        if y == 0:
            return [(1.0, (x - 1, 0, N - 1))]
        else:
            return [(beta, (x - 1, y - 1, N - 1)), (1.0 - beta, (x - 1, y, N - 1))]
    elif policy == 2:
        assert(y == 0 and x > 0)
        return [(beta, (x - 1, M - 1, phi(z))), (1.0 - beta, (x - 1, M, phi(z)))]
    elif policy == 3:
        assert(x > 1 and y == 0 and z == 0)
        return [(beta, (x - 2, M - 1, N - 1)), (1.0 - beta, (x - 2, M, N - 1))]


def get_transitions(state):
    policies = get_policy_candidates(state)

    res = []
    for p in policies:
        states = get_outcomes_for_policy(state, p)
        for s in states:
            x, y, z = s[1]
            res.append((alpha * s[0], (x + 1, y, z)))
            res.append(((1 - alpha) * s[0], (x, y, z)))

    return res


adj_list = {}


def run(N, M, Q):
    for i in range(Q + 1):
        for j in range(M + 1):
            for k in range(N):
                adj_list[(i, j, k)] = []

    for i in range(Q + 1):
        for j in range(M + 1):
            for k in range(N):
                if i == Q:
                    adj_list[(i, j, k)] = [(1.0, (0, 0, 0))]
                    continue

                transitions = get_transitions((i, j, k))
                for t in transitions:
                    adj_list[(i, j, k)].append(t)


def sft(t):
    return [x[1] for x in t]


def generated_edges():
    edges = []
    for state in adj_list:
        add = [s[1] for s in adj_list[state]]
        from formula_edge_generator import edgize
        add = edgize(state, add)
        edges += add

    return set(edges)


if __name__ == "__main__":
    run(N, M, Q)
    from formula_edge_generator import FormulaEdgeGenerator
    feg = FormulaEdgeGenerator(Q=500, M=10, N=20)
    edges = feg.get_edges_based_on_formula()
    edges2 = generated_edges()
    print(len(edges.difference(edges2)))
    print(len(edges2.difference(edges)))
