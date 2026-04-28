import unittest
import SearchEngine.Rank as Rank
from model import Recipe as recipe

class TestRankNewest(unittest, Rank):

    def test_no_recipe_list(self):
        r : Rank= Rank()
        self.assertEqual(r.rank_by_newest([]),[])
        pass

    def test_one_recipe_item(self):
        pass

    def test_is_sorted(self):
        pass