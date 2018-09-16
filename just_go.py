from initialize import Initialize
from fitness import Fitness
from select import Select
from crossover import Crossover
from mutate import Mutate


class JustGo:
    def __init__(self):
        pass

    @staticmethod
    def go(n, size):
        gene_codes = Initialize.initialize(n, size)

