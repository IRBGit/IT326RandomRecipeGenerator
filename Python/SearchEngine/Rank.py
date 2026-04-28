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
        recipe_list.sort(key=lambda recipe: recipe.published_time)
        return recipe_list

    # returns a sorted list of recipes by how popular they are
    #note: do not have popularity saved in recipe so it just returns a list, unsorted
    #By: Alysa Solomon
    def rank_by_popularity(self, recipe_list: List[Recipe]):
        return recipe_list
