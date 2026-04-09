from model import Recipe
from typing import List
from datetime import datetime
class Rank:

    # returns a sorted list of recipes by time
    def rank_by_newest(self, recipe_list: List[Recipe]):
        if len(recipe_list) <= 1:
            return recipe_list
        sorted = recipe_list.sort(Recipe.published_time)
        return sorted