"""
Test checking FreeBet object instantiate the registering and login screens
before displaying the login one.
"""
from freebet import FreeBet

class TestFreeBet:
    object_to_test = FreeBet()

    def test_build_method(self):
        self.object_to_test.build()
        assert len(self.object_to_test.display.screens) == 2
        assert self.object_to_test.display.screen_names[0] == "login"
        assert self.object_to_test.display.screen_names[1] == "register"
        assert self.object_to_test.display.current == "login"
