import random


class Methods:
    def __init__(self, population: list, is_min: bool = False):
        self.population = population
        self.is_min = is_min
        self.il = len(population)

    def calc(self):
        raise NotImplementedError("Method calc is not implemented")


class RouletteMethod(Methods):
    def set_min_eval_attribute(self) -> None:
        max_value = max([p["eval"] for p in self.population])
        for p in self.population:
            p["min_eval"] = max_value - p["eval"] + 1

    def calc_sum_of_eval(self, type_of_eval: str = "eval") -> float:
        return sum([p[type_of_eval] for p in self.population])

    def calc_probability(self, type_of_eval: str) -> None:
        sum_of_eval = self.calc_sum_of_eval(type_of_eval)
        for p in self.population:
            p["probability"] = p[type_of_eval] / sum_of_eval

    def cumulative_distribution(self) -> None:
        cum_dist = 0
        for p in self.population:
            cum_dist += p["probability"]
            p["q"] = cum_dist

    def clear_population(self):
        [p.pop("min_eval", None) for p in self.population]

    def calc(self) -> list:
        type_of_eval = "min_eval" if self.is_min else "eval"
        if self.is_min:
            self.set_min_eval_attribute()
        self.calc_probability(type_of_eval)
        self.cumulative_distribution()
        self.clear_population()

        out = []
        while len(out) < self.il:
            chosen = None
            r = random.random()
            for p in self.population:
                chosen = p
                if r <= p["q"]:
                    break
            out.append(chosen)
        return out


class RankingMethod(Methods):
    def calc(self) -> list:
        population = sorted(self.population, key=lambda p: p["eval"], reverse=(not self.is_min))
        out = []
        while len(out) < self.il:
            rand_first_num = random.choice(range(1, self.il + 1))
            rand_index = random.choice(range(rand_first_num))
            out.append(population[rand_index])
        return out


class TournamentMethod(Methods):
    def __init__(self, population: list, is_min: bool = False, without_return: bool = False):
        super(TournamentMethod, self).__init__(population=population, is_min=is_min)
        self.without_return = without_return

    def calc(self) -> list:
        # Size of single group
        j = 3
        out = []
        while len(out) < self.il:
            group = []
            while len(group) < j:
                rand_index = random.choice(range(self.il))
                single_person = self.population[rand_index]
                if not self.without_return or (self.without_return and single_person not in group):
                    group.append(single_person)
            chosen_person = min(group, key=lambda p: p["eval"]) if self.is_min else max(group, key=lambda p: p["eval"])
            out.append(chosen_person)
        return out
