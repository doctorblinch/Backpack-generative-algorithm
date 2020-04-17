from backpack_state import Backpack
from offspring import Offsrping
import numpy as np

P = np.array([10, 7, 23, 8, 14, 28, 11, 15, 14, 15, 20, 23])
W = np.array([8, 5, 4, 4, 15, 18, 6, 10, 17, 12, 9, 16])
w = 50
N = 15

if __name__ == '__main__':
    backpack = Backpack(W, P, w, N)
    backpack.initial_generate_offsprings()
    for i in backpack.offsprings:
        print(i.get_weight(backpack.W))
    print('Starting state')
    print(backpack)

    for i in range(5):
        backpack.generate_offsprings()

        backpack.reanimate()

        backpack.mutate()

        backpack.reanimate()

        backpack.local_upgrade()

        backpack.leave_best_offsprings()

        print('Iteration #{}\n'.format(i+1))
        print(backpack)
