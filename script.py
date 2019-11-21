import copy
import random

from population import Population


class Crossover:
    def __init__(self, population):
        self.population = copy.deepcopy(population)
        self.pk = 0.5
        self.pairs = []

    def select_pairs(self):
        chosen = list(filter(lambda p: random.random() >= self.pk, self.population))
        self.population = list(filter(lambda p: p not in chosen, self.population))
        if len(chosen) % 2:
            r = random.randint(0, len(self.population) - 1)
            chosen.append(self.population.pop(r))
        while len(chosen):
            first_chromosome = chosen.pop(0)
            r = random.randint(0, len(chosen) - 1)
            second_chromosome = chosen.pop(r)
            self.pairs.append([first_chromosome, second_chromosome])

    def merge_lists(self, gens):
        tmp = []
        for g in gens:
            tmp = tmp + g
        return tmp

    def calc(self):
        self.select_pairs()


class KPointCrossover(Crossover):
    def __init__(self, population, n=1):
        super().__init__(population)
        self.n = n

    def calc(self):
        super().calc()
        # debug_population(self.pairs[0])
        print()
        for pair in self.pairs:
            gens_one = []
            gens_two = []
            sum_m = 0

            for chromosome in pair[0]["chromosomes"]:
                sum_m += chromosome["m"]
                gens_one += chromosome["gens"]
            for chromosome in pair[1]["chromosomes"]:
                gens_two += chromosome["gens"]

            # if not self.n:
            #     self.n = random.randint(1, sum_m - 1)

            new_gens_one = []
            new_gens_two = []
            rand_points = [0]
            for _ in range(self.n):
                r = random.randint(rand_points[len(rand_points) - 1] + len(rand_points) - 1,
                                   sum_m - (self.n + len(rand_points) - 1))
                rand_points.append(r)
            print()
            print(rand_points[1:])
            for i in range(1, len(rand_points)):
                start_point = rand_points[i - 1]
                end_point = rand_points[i]
                new_gens_one.append(gens_one[start_point:end_point])
                new_gens_two.append(gens_two[start_point:end_point])

            new_gens_one.append(gens_one[rand_points[len(rand_points) - 1]:])
            new_gens_two.append(gens_two[rand_points[len(rand_points) - 1]:])

            print(new_gens_one)
            print(new_gens_two)
            print()
            should_cross = False
            for i in range(len(new_gens_one)):
                if should_cross:
                    tmp = copy.deepcopy(new_gens_one[i])
                    new_gens_one[i] = copy.deepcopy(new_gens_two[i])
                    new_gens_two[i] = copy.deepcopy(tmp)
                should_cross = not should_cross

            print(new_gens_one)
            print(new_gens_two)
            new_gens_one = self.merge_lists(new_gens_one)
            new_gens_two = self.merge_lists(new_gens_two)

            for chromosome in pair[0]["chromosomes"]:
                chromosome["gens"] = new_gens_one[:chromosome["m"]]
                new_gens_one = new_gens_one[chromosome["m"]:]
            for chromosome in pair[1]["chromosomes"]:
                chromosome["gens"] = new_gens_two[:chromosome["m"]]
                new_gens_two = new_gens_two[chromosome["m"]:]
        # debug_population(self.pairs[0])
        for pair in self.pairs:
            self.population.append(pair[0])
            self.population.append(pair[1])
        return self.population


class UniformCrossover(Crossover):
    def calc(self):
        super().calc()
        for pair in self.pairs:
            gens_one = []
            gens_two = []
            sum_m = 0

            for chromosome in pair[0]["chromosomes"]:
                sum_m += chromosome["m"]
                gens_one += chromosome["gens"]
            for chromosome in pair[1]["chromosomes"]:
                gens_two += chromosome["gens"]

            template = [random.choice([0, 1]) for _ in range(sum_m)]
            child_one = {
                0: gens_one,
                1: gens_two
            }
            child_two = {
                0: gens_two,
                1: gens_one
            }
            print()
            print(gens_one)
            print(gens_two)
            print()
            gens_one = [child_one[g][index] for index, g in enumerate(template)]
            gens_two = [child_two[g][index] for index, g in enumerate(template)]
            print(gens_one)
            print(gens_two)
            print()

            for chromosome in pair[0]["chromosomes"]:
                chromosome["gens"] = gens_one[:chromosome["m"]]
                gens_one = gens_one[chromosome["m"]:]
            for chromosome in pair[1]["chromosomes"]:
                chromosome["gens"] = gens_two[:chromosome["m"]]
                gens_two = gens_two[chromosome["m"]:]
        for pair in self.pairs:
            self.population.append(pair[0])
            self.population.append(pair[1])
        return self.population


def debug_population(population) -> None:
    for p in population:
        print([chromosome["gens"] for chromosome in p["chromosomes"]])


def main():
    n_dimension = 3
    d = 6
    a = -1
    b = 1
    il = 10

    arr_n = [
        {"a": -1, "b": 1, "d": 6},
        {"a": -2, "b": 2, "d": 7},
        {"a": -3, "b": 0, "d": 3},
    ]

    population = (Population(n_dimension, a, b, d, il, arr_n)).generate_population()
    k_point = KPointCrossover(population, n=1)
    k_point.calc()
    # uniform = UniformCrossover(population)r
    # uniform.calc()


if __name__ == "__main__":
    main()
