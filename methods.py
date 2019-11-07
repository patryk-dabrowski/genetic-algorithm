import random


class Methods:
    def __init__(self, population: list, is_min: bool = False):
        self.population = population
        self.is_min = is_min
        self.il = len(population)

    def calc(self):
        raise NotImplementedError("Method calc is not implemented")


class SelectMethod(Methods):
    def set_fit_attribute(self) -> None:
        self.population = [{"fit": p} for p in self.population]

    def calc_sum_of_fit(self) -> float:
        return sum([p["fit"] for p in self.population])

    def calc_probability(self) -> None:
        sum_of_fit = self.calc_sum_of_fit()
        for p in self.population:
            p["probability"] = p["fit"] / sum_of_fit

    def cumulative_distribution(self) -> None:
        cum_dist = 0
        for p in self.population:
            cum_dist += p["probability"]
            p["q"] = cum_dist

    def calc(self) -> list:
        self.set_fit_attribute()
        self.calc_probability()
        self.cumulative_distribution()

        out = []
        while len(out) < self.il:
            chosen = None
            r = random.random()
            for p in self.population:
                chosen = p["fit"]
                if r <= p["q"]:
                    break
            out.append(chosen)
        return out


class RankingMethod(Methods):
    def calc(self) -> list:
        population = sorted(self.population, reverse=(not self.is_min))
        out = []
        while len(out) < self.il:
            rand_first_num = random.choice(range(1, self.il + 1))
            rand_index = random.choice(range(rand_first_num))
            out.append(population[rand_index])
        return out


class TournamentMethod(Methods):
    def __init__(self, population: list, is_min: bool = False, without_return=False):
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
                if not self.without_return or (
                    self.without_return and single_person not in group
                ):
                    group.append(single_person)
            chosen_person = min(group) if self.is_min else max(group)
            out.append(chosen_person)
        return out
