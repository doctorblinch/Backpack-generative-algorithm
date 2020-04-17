import numpy as np
from random import choice
from offspring import Offsrping


class Backpack:
    def __init__(self, W, P, w, N):
        assert len(W) == len(P)
        self.W = np.array(W)
        self.P = np.array(P)
        self.L = len(W)
        self.N = N
        self.w = w
        self.mutation_p = 1 / (4 * self.L)
        self.offsprings = []

    def __repr__(self):
        s = ''
        for i in self.offsprings:
            s += 'Metrics = {} {}'.format(str(i.count_metrics(self.P)), str(i))

        return s

    def initial_generate_offsprings(self, random_seed=-1):
        if random_seed != -1:
            np.random.seed(random_seed)

        while len(self.offsprings) < self.N:
            tmp = Offsrping(X=np.random.randint(2, size=self.L))

            can_add = True
            for j in self.offsprings:
                if tmp == j:
                    can_add = False
                    break

            if can_add:
                self.offsprings.append(tmp)

    def get_parents_pairs4breeding(self) -> list:
        assert self.N == len(self.offsprings)

        pairs = []
        taken = np.zeros([1, self.N])[0]
        zero = np.where(taken == 0)[0]

        for _ in range(self.N // 2):
            current = choice(zero)
            zero = np.delete(zero, np.argwhere(zero == current))
            taken[current] = 1

            outbreed_index = -1
            outbreed_value = -1
            for i in zero:
                v = np.absolute(self.offsprings[current].X - self.offsprings[i].X).sum()
                if v > outbreed_value:
                    outbreed_value = v
                    outbreed_index = i

            pairs.append((current, outbreed_index))
            taken[outbreed_index] = 1
            zero = np.delete(zero, np.argwhere(zero == outbreed_index))

        return pairs

    def create_offspring(self, parent1: Offsrping, parent2: Offsrping) -> Offsrping:
        X1 = parent1.X
        X2 = parent2.X

        X = X1 * X2

        for i in range(self.L):
            if X1[i] != X2[i]:
                norm_metrics = parent1.count_metrics(self.P) + parent2.count_metrics(self.P)
                X[i] = np.random.choice([X1[i], X2[i]],
                                        p=[parent1.metrics / norm_metrics, parent2.metrics / norm_metrics])

        # self.offsprings.append(Offsrping(X=X))
        return Offsrping(X=X)

    def generate_offsprings(self, add=True):
        pairs = self.get_parents_pairs4breeding()

        offsprings = []

        for i, j in pairs:
            offspring = self.create_offspring(
                self.offsprings[i], self.offsprings[j]
            )

            if not add:
                offsprings.append(offspring)
            else:
                self.offsprings.append(offspring)

            if not add:
                return offsprings

    def mutate(self):
        for offspring in self.offsprings:
            offspring.mutate(self.mutation_p)

    def local_upgrade(self):
        for offspring in self.offsprings:
            offspring.local_upgrade(self.w, self.W)

    def reanimate(self):
        for offspring in self.offsprings:
            offspring.reanimate(self.w, self.P, self.W)

    def leave_best_offsprings(self):
        self.offsprings.sort(key=lambda x: x.count_metrics(self.P))
        self.offsprings = self.offsprings[-self.N:]
