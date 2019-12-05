import copy
import random


class Mutation:
    def __init__(self, population):
        self.population = population
        self.pm = 0.1

    def execute(self):
        population = copy.deepcopy(self.population)
        out_population = []
        for p in population:
            is_changed = False
            for chromosome in p["chromosomes"]:
                gens = []
                for gen in chromosome["gens"]:
                    r = random.random()
                    if r < self.pm:
                        gen = 0 if gen == 1 else 1
                        is_changed = True
                    gens.append(gen)
                chromosome["gens"] = gens
            if is_changed:
                out_population.append(p)
        return out_population


class Inversion:
    def __init__(self, population):
        self.population = population
        self.pi = 0.1

    def execute(self):
        population = copy.deepcopy(self.population)
        out_population = []
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
                out_population.append(p)
        return out_population


class Crossover:
    def __init__(self, population, *args, **kwargs):
        self.population = copy.deepcopy(population)
        self.pk = 0.5
        self.pairs = []

    def select_pairs(self):
        chosen = []
        other_population = []

        for p in self.population:
            r = random.random()
            if r >= self.pk:
                chosen.append(p)
            else:
                other_population.append(p)
        if len(chosen) % 2:
            r = random.randint(0, len(other_population) - 1)
            chosen.append(other_population.pop(r))
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

    def sum_attribute(self, chromosomes, attribute, sum_value):
        for chromosome in chromosomes:
            sum_value += chromosome[attribute]
        return sum_value

    def calc(self):
        raise NotImplementedError("Method should be implemented")

    def execute(self):
        self.select_pairs()
        self.calc()
        out_population = []
        for pair in self.pairs:
            out_population.append(pair[0])
            out_population.append(pair[1])
        return out_population


class KPointCrossover(Crossover):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.k = kwargs.get("k", None)

    def calc(self):
        for pair in self.pairs:
            sum_m = self.sum_attribute(pair[0]["chromosomes"], "m", 0)
            gens_one = self.sum_attribute(pair[0]["chromosomes"], "gens", [])
            gens_two = self.sum_attribute(pair[1]["chromosomes"], "gens", [])

            if not self.k:
                self.k = random.randint(1, sum_m - 1)

            new_gens_one = []
            new_gens_two = []
            rand_points = [0]
            for _ in range(self.k):
                last_element = rand_points[len(rand_points) - 1]
                r = random.randint(last_element + 1, sum_m - self.k + len(rand_points) - 1)
                rand_points.append(r)
            for i in range(1, len(rand_points)):
                start_point = rand_points[i - 1]
                end_point = rand_points[i]
                new_gens_one.append(gens_one[start_point:end_point])
                new_gens_two.append(gens_two[start_point:end_point])

            new_gens_one.append(gens_one[rand_points[len(rand_points) - 1]:])
            new_gens_two.append(gens_two[rand_points[len(rand_points) - 1]:])

            should_cross = False
            for i in range(len(new_gens_one)):
                if should_cross:
                    tmp = copy.deepcopy(new_gens_one[i])
                    new_gens_one[i] = copy.deepcopy(new_gens_two[i])
                    new_gens_two[i] = copy.deepcopy(tmp)
                should_cross = not should_cross

            new_gens_one = self.merge_lists(new_gens_one)
            new_gens_two = self.merge_lists(new_gens_two)

            for chromosome in pair[0]["chromosomes"]:
                chromosome["gens"] = new_gens_one[:chromosome["m"]]
                new_gens_one = new_gens_one[chromosome["m"]:]
            for chromosome in pair[1]["chromosomes"]:
                chromosome["gens"] = new_gens_two[:chromosome["m"]]
                new_gens_two = new_gens_two[chromosome["m"]:]


class UniformCrossover(Crossover):
    def calc(self):
        for pair in self.pairs:
            sum_m = self.sum_attribute(pair[0]["chromosomes"], "m", 0)
            gens_one = self.sum_attribute(pair[0]["chromosomes"], "gens", [])
            gens_two = self.sum_attribute(pair[1]["chromosomes"], "gens", [])

            template = [random.choice([0, 1]) for _ in range(sum_m)]
            child_one = {
                0: gens_one,
                1: gens_two
            }
            child_two = {
                0: gens_two,
                1: gens_one
            }
            gens_one = [child_one[g][index] for index, g in enumerate(template)]
            gens_two = [child_two[g][index] for index, g in enumerate(template)]

            for chromosome in pair[0]["chromosomes"]:
                chromosome["gens"] = gens_one[:chromosome["m"]]
                gens_one = gens_one[chromosome["m"]:]
            for chromosome in pair[1]["chromosomes"]:
                chromosome["gens"] = gens_two[:chromosome["m"]]
                gens_two = gens_two[chromosome["m"]:]