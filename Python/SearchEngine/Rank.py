from model import Recipe
from typing import List
from datetime import datetime
class Rank:

    # returns a sorted list of recipes by time
    #By: Alysa Solomon
    def rank_by_newest(self, recipe_list: List[Recipe]):
        if len(recipe_list) <= 1:
            return recipe_list
        # recipe_list.sort()
        recipe_list.sort()
        return recipe_list


