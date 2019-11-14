import copy
import random


class Mutation:
    def __init__(self, population):
        self.population = population
        self.pm = 0.1

    def calc(self):
        population = copy.deepcopy(self.population)
        for p in population:
            for chromosome in p["chromosomes"]:
                gens = []
                for gen in chromosome["gens"]:
                    r = random.random()
                    if r < self.pm:
                        gen = 0 if gen == 1 else 1
                    gens.append(gen)
                chromosome["gens"] = gens
        return population


class Inversion:
    def __init__(self, population):
        self.population = population
        self.pi = 0.1

    def calc(self):
        population = copy.deepcopy(self.population)
        for p in population:
            r = random.random()
            if r < self.pi:
                gens = []
                sum_m = 0
                for chromosome in p["chromosomes"]:
                    sum_m += chromosome['m']
                    gens += chromosome["gens"]

                a = random.randint(0, sum_m - 2)
                b = random.randint(a + 1, sum_m - 1)

                new_gens = [gens[:a], gens[a:b], gens[b:]]
                new_gens[1].reverse()
                new_gens = new_gens[0] + new_gens[1] + new_gens[2]

                for chromosome in p["chromosomes"]:
                    chromosome["gens"] = new_gens[:chromosome["m"]]
                    new_gens = new_gens[chromosome["m"]:]
        return population
