from kivy.lang.builder import Builder

###Load screens kv files code###
Builder.load_file('screens/login/loginscreen.kv')
Builder.load_file('screens/register/registerscreen.kv')
Builder.load_file('screens/bet/bettingscreen.kv')

###Load pages kv files code###
Builder.load_file('screens/bet/pages/matchselection/selectionpages.kv')
Builder.load_file('screens/bet/pages/match/matchpage.kv')
Builder.load_file('screens/bet/pages/bet/betpage.kv')
Builder.load_file('screens/bet/pages/bestplayers/bestplayerspage.kv')

###Load buttons kv files code###
Builder.load_file('screens/bet/buttons/buttons.kv')
