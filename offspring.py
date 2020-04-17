import numpy as np


class Offsrping:
    def __init__(self, n=1, X=None):
        self.n = n

        if X is None:
            self.X = np.array([0 for _ in range(n)])
        else:
            self.X = np.array(X)
            self.n = len(X)

        self.metrics = -1

    def __repr__(self):
        return "State({})\n".format(self.X)

    def __eq__(self, other):
        if isinstance(other, Offsrping):
            return np.array_equal(other.X, self.X)

        return False

    def count_metrics(self, P) -> np.int64:
        m = self.X.dot(P.T)
        self.metrics = m
        return m

    def reanimate(self, w, P, W):
        while self.X.dot(W.T) > w:
            prices_of_picked = [P[i] if self.X[i] == 1 else 1000 for i in range(self.n)]
            index = prices_of_picked.index(min(prices_of_picked))
            self.X[index] = 0

    def mutate(self, mutation_p):
        for i in range(self.n):
            if np.random.choice([True, False], p=[mutation_p, 1 - mutation_p]):
                self.X[i] = 1 - self.X[i]

    def local_upgrade(self, w, W):
        while True:
            weights_of_picked = [W[i] if self.X[i] == 0 else 1000 for i in range(self.n)]
            index = weights_of_picked.index(min(weights_of_picked))
            self.X[index] = 1
            if self.X.dot(W.T) > w:
                self.X[index] = 0
                return

    def get_weight(self, W):
        return self.X.dot(W.T)
