# Freebet
![MainPage](/images/FreeBet.png)

This app purpose is to allow players to bet for free on their phone or on their computer.

## Installing

To install the app, you have two available solutions:

* If you have a phone using android, you can dowload the apk at this address: http://206.189.118.233/download (you will need to add .apk to the file once downloaded if the extension is missing)

* Or install it on your computer following those steps:

```
  - git clone https://github.com/Nivose44/BookMarket.git
  - cd BookMarket
  - pip install pipenv
  - sudo apt-get install python3-pip
  - sudo apt-get install cython3 python3-dev
  - sudo apt-get install libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev
  - python -m pip install git+https://github.com/kivy/kivy.git@master
  - pipenv install
```
## How to use
Freebet contains two main functionnalities and and two main sort of bets.
Bets are either public or private; it means they have either been scraped or have been created by other users.
To display public bets which come from scraped informations, you need to select one of the sports displayed once logged in, and select the region and competitions you want to display related matches from. Once done, matches will be displayed under this format:

![Matches](/images/Matches.png)

You can then enter the amount you want to bet and use press the button related to the match, or use the bottom button to create a private bet about this match.

![CreateBet](/images/CreateBet.png)

As you can see, the bet creation popup awaits you to select the outcome you want to create a bet for, to enter an odd players will bet on, and the limit amount users will be able to bet.
** Important: ** when creating a bet, the amount that will be taken off your account isn't the limit you are fixing, but the the limit time the odd, because you need to be able to pay other players in case they win the bet you created. If my odd for Manchester City was 2 and my limit 50, 100 would be taken off my account untill the game is played

To display and bets on those private bets, you just need to go back to the main page and press the private bets button:

![Private](/images/Private.png)

## Built With

* [Kivy](https://kivy.org/#home)
* [Scrapy](https://scrapy.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
