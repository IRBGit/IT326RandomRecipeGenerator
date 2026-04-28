import unittest
import SearchEngine.Rank as Rank
from model import Recipe as recipe
import datetime as dt
from random import shuffle

#By Alysa Solomon
class TestRankNewest(unittest.TestCase):

    def test_no_recipe_list(self):
        r : Rank.Rank= Rank.Rank()
        self.assertEqual(r.rank_by_newest([]),[])
        pass

    def test_one_recipe_item(self):
        r : Rank.Rank= Rank.Rank()
        reci = recipe("Apples",["Apples"],["Cut them up","Eat"],dt.datetime.now())
        self.assertEqual(r.rank_by_newest([reci]),[reci])
        pass

        #I Don't Understand
    def test_is_sorted(self):
        r : Rank.Rank= Rank.Rank()
        
        with self.subTest():
            item_list = ["Apples","Cucumbers","Kiwi","Fruit","Bannana"]
            recipe_list = [recipe(item_list[i],[item_list[i]],["Cut them up","Eat"],dt.datetime.now()) for i in range(len(item_list))]
            sorted = recipe_list
            shuffle(recipe_list)
            self.assertEqual(r.rank_by_newest(recipe_list), sorted)
        pass

if __name__ == '__main__':
    unittest.main()