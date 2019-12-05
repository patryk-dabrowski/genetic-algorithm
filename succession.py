import random


class Succession(object):
    def __init__(self, parents, children, is_min=False):
        self.parents = parents
        self.children = children
        self.number_of_population = len(self.parents)
        self.is_min = is_min

    def get_sorted_and_unique(self, items):
        out = list({v["eval"]: v for v in items}.values())
        out = sorted(out, key=lambda p: p["eval"], reverse=not self.is_min)
        return out

    def execute(self):
        raise NotImplementedError("Method execute() must be implemented")


class TriviaSuccession(Succession):
    def execute(self):
        population = sorted(self.children, key=lambda p: p["eval"], reverse=not self.is_min)
        return population[:self.number_of_population]


class PartialSuccession(Succession):
    def execute(self):
        parents = self.get_sorted_and_unique(self.parents)
        children = self.get_sorted_and_unique(self.children)

        proportion = round(self.number_of_population * 0.5)
        return parents[:proportion] + children[:proportion]


class EliteSuccession(Succession):
    def execute(self):
        altogether = self.get_sorted_and_unique(self.parents + self.children)
        return altogether[:self.number_of_population]


class CompressionSuccession(Succession):
    def execute(self):
        altogether = self.get_sorted_and_unique(self.parents + self.children)
        precision = 10

        while len(altogether) > self.number_of_population:
            for i in range(len(altogether), 0, -1):
                curr = round(altogether[i - 1]["eval"], precision)

                if curr in [round(a["eval"], precision) for index, a in enumerate(altogether) if i - 1 != index]:
                    altogether.pop(i - 1)

                if len(altogether) == self.number_of_population:
                    break
            precision -= 1
        return altogether


class RandomSuccession(Succession):
    def execute(self):
        altogether = self.parents + self.children
        while len(altogether) > self.number_of_population:
            r = random.randint(0, len(altogether) - 1)
            altogether.pop(r)

        return altogether
