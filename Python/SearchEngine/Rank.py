from model import Recipe
from typing import List
from datetime import datetime
class Rank:

    # returns a sorted list of recipes by time
    #By: Alysa Solomon
    def rank_by_newest(self, recipe_list: List[Recipe]):
        recipes_with_time = []
        recipes_no_time = []
        for recipe in recipe_list:
            if recipe.published_time != None:
                recipes_with_time.append(recipe)
            else:
                recipes_no_time.append(recipe)
        

        if len(recipe_list) <= 1:
            return recipe_list
        # recipe_list.sort()
        recipes_with_time.sort(key=lambda recipe: recipe.published_time)
        recipe_list = recipes_with_time + recipes_no_time
        return recipe_list

    # returns a sorted list of recipes by how popular they are
    #note: do not have popularity saved in recipe so it just returns a list, unsorted
    #By: Alysa Solomon
    def rank_by_popularity(self, recipe_list: List[Recipe]):
        return recipe_list
