import time
import operator
import random


class BestSolution (object):

    def __init__(self, maxsize, best=(0, 0)):
        self.maxsize = maxsize
        self.worse_sol, self.worse_value = best
        self._db = {
            best[0] : best[1]
        }

    def __len__(self):
        return len(self._db)

    @property
    def values (self):
        return list(self._db.values())

    def update (self, sol, value):
        if self._db.__len__() < self.maxsize:
            self._db[sol] = value
            if value < self.worse_value:
                self.worse_value, self.worse_sol = value, sol
        else:
            if value > self.worse_value:
                self._db.pop(self.worse_sol)
                self._db[sol] = value
                self.worse_sol, self.worse_value = min(self._db.items(), key=operator.itemgetter(1))




class Node (object):

    def __init__(self, root, item, next_items, is_root = False):
        self.root = root
        self.item = item
        self.value = 0 if is_root else (root.value + item)
        self.UB = sum(filter(lambda i: i > 0, next_items)) + self.value
        self.bound = False
        self.done = False
        self.leaf = True if len(next_items) == 0 else False
        self.child = self.child_generator(next_items) if not self.leaf else None

    def child_generator (self, items):
        L = len(items) - 1
        for n, i in enumerate(items):
            if n == L:
                self.done = True
            yield Node(self, i, items[n + 1:])

    def __repr__(self):
        return str(self.__dict__)


class Tree (object):

    def __init__(self, items):
        self.root = Node(None, None, tuple(items), is_root=True)

    def __call__(self, k):
        cnode = self.root
        best = BestSolution(maxsize=k, best=(self.root, self.root.value))

        while True:

            #print(cnode, end="\n\n\n")

            if cnode == self.root and cnode.done:
                break

            if cnode.leaf or cnode.bound or cnode.done:
                cnode = cnode.root
            else:
                cnode = next(cnode.child)
                value = cnode.value
                best.update(cnode, value)

                if cnode.UB < best.worse_value:
                    cnode.bound = True

        return best


def random_problem(size):
    options = list(range(-100, +100))
    assert size < len(options)
    return random.sample(options, size), random.randint(1, size - 1)

if __name__ == "__main__":
    items, k = random_problem(10)
    #items, k = [ 6, 3, 0, -3, -7, -20], 4

    tree = Tree(items)
    start = time.time()
    best = tree.__call__(k)

    print("Items: ", items)
    print("K: ", k)
    print("Time: ", time.time() - start)
    print("Best solutions cost: ", best.values)

    #
