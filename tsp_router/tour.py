from typing import List, Dict

Tour = List[int]


class Tour:

    def __init__(self):
        pass

    @staticmethod
    def convert_tour(tour: Tour) -> Dict[int, List[int]]:
        new_tour = {}
        for i in range(len(tour)):
            new_tour[tour[i - 1]] = [tour[i - 2], tour[i]]
        return new_tour
