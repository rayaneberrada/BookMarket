"""
File testing the right behavior of bestplayers.py
"""
from screens.bet.pages.bestplayers.bestplayerspage import BestPlayerPage

class TestBestPLayers:
    """
    Class managing the test for the BestPlayerPage class
    """
    response = {'winners': [{'argent': 1000, 'nom': 'miguel'},
                            {'argent': 1000, 'nom': 'aa'},
                            {'argent': 1000, 'nom': 'Rayane\t'}]}

    def test_parse_json(self):
        """
        Check the parser follow the right behavior and display the informations
        sent by back to the request made to the API
        """
        bestplayers = BestPlayerPage()
        bestplayers.parse_json(None, self.response)
        assert bestplayers.children[0].text == "Rayane\t est 3 avec un total de 1000"
        assert len(bestplayers.children) == 3
