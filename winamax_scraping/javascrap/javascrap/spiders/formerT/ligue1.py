import subprocess, pytest
import json

@pytest.yield_fixture
def setItemsFile():
	f = open("/home/rayane/Programmation/BettingApp/ScrappyTries/javascrap/javascrap/spiders/l1_items.json", "r")
	items = json.load(f)
	items = items[0]
	g = open("/home/rayane/Programmation/BettingApp/ScrappyTries/javascrap/javascrap/spiders/ligue1_2019_2020.json", "r")
	teams = json.load(g)
	teams = teams["teams"]
	yield items, teams

class TestLigueUn:
	def testItems(self, setItemsFile):
		items, teams = setItemsFile
		matches = []
		for day in items["home"]:
			for home_team in day:
				assert home_team in teams
				matches.append(home_team)
		for day in items["away"]:
			for away_team in day:
				assert away_team in teams
				matches.append(away_team)
		for day in range(len(items["home"])):
			assert len(items["home"][day]) == len(items["away"][day])
		assert len(items["home"]) >= 1
		assert len(items["time"]) == len(matches)/2
		assert len(items["broadcasters"]) == len(matches)/2