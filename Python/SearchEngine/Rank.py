from model import Recipe
from typing import List
from datetime import datetime
class Rank:

    # returns a sorted list of recipes by time
    def rank_by_newest(self, recipe_list: List[Recipe]):
        return recipe_list