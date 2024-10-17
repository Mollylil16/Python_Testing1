import unittest
from server import loadClubs, loadCompetitions

class TestApp(unittest.TestCase):
    def test_loadClubs(self):
        clubs = loadClubs()
        self.assertIsInstance(clubs, list)
        self.assertGreater(len(clubs), 0)
    
    def test_loadCompetitions(self):
        competitions = loadCompetitions()
        self.assertIsInstance(competitions, list)
        self.assertGreater(len(competitions), 0)

if __name__ == '__main__':
    unittest.main()