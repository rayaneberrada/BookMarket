# -*- coding: utf-8 -*-
import scrapy, json, re, datetime, time
from javascrap.items import MatchItem
from urllib.parse import urljoin
import time




class WinamaxrugbySpider(scrapy.Spider):
    name = 'winamaxScraping'
    allowed_domains = ['web']
    download_delay = 2.0
    start_urls = ['https://www.winamax.fr/paris-sportifs/sports']

    def parse(self, response):
        """
        The parsing function will go through the html page donwloaded and extrat informations
        we are interested in
        """
        self.start_time = time.time()
        sports_to_scrap = ["Football", "Basketball", "Tennis", "Rugby"]
        # This variable will allow us to have the same scraped time for every matches
        datas = self.turn_to_json(response)

        for sport_id in datas["sportIds"]:
            sport_id = str(sport_id)
            if datas["sports"][sport_id]["sportName"] in sports_to_scrap:
                #We define here which sport we are going to scrap
                regions = datas["sports"][sport_id]["categories"]        
                for region_id in regions:
                    competitions = datas["categories"][str(region_id)]["tournaments"]
                    region_name = datas["categories"][str(region_id)]["categoryName"]
                    # Informations are loaded in the html files depending of the url.
                    # For exemple https://www.winamax.fr/paris-sportifs/sports/1 is referring to football.
                    # It means that we need to look through every single region url reference and every
                    # competition related to get all the informations we need.
                    # For exemple with: https://www.winamax.fr/paris-sportifs/sports/1/7/884 
                    # 7 refers to France datas and 884 to the Coupe de la ligue datas.
                    # Scraping this url will allow us to access matches and odds related to that competition
                    for competition_id in competitions:
                        url = sport_id + "/" + str(region_id) + "/" + str(competition_id)
                        yield scrapy.Request(urljoin('https://www.winamax.fr/paris-sportifs/sports/', url),\
                                                    callback=self.parse_matches,\
                                                    cb_kwargs=dict(competition=str(competition_id), region=region_name, sport_id = sport_id),\
                                                    dont_filter=True,
                                                    headers={"User-Agent":"berradarayane@gmail.com"})

    def parse_matches(self, response, competition, region, sport_id):
        """
        Extract the datas about a match that will be added to the database
        """
        item = MatchItem()
        datas = self.turn_to_json(response)
        matches = datas["tournaments"][competition]["matches"]

        for match_id in matches:
            match_datas = datas["matches"][str(match_id)]
            item["home"] = match_datas["competitor1Name"]
            item["away"] = match_datas["competitor2Name"]
            item["region"] = region
            item["time_scraped"] = datetime.datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')

            if "tvChannels" in match_datas:
                item["broadcasters"] = match_datas["tvChannels"] 
            else:
                item["broadcasters"] = None

            item["sport"] = datas["sports"][sport_id]["sportName"]
            item["url"] = response.url
            item["bookmaker"] = "Winamax"
            item["league"] = datas["tournaments"][competition]["tournamentName"]
            item["playing_time"] = datetime.datetime.fromtimestamp(match_datas["matchStart"]).strftime('%Y-%m-%d %H:%M:%S')

            bet_id = str(match_datas["mainBetId"])
            odds_id = datas["bets"][bet_id]["outcomes"]
            item["odd_draw"] = None
        
            if len(datas["bets"][bet_id]["outcomes"]) not in [2, 3]:
                print("The bet n° " + bet_id + " at url: " + response.url + " isn't a match")
                continue

            for odd in odds_id:
                team_code = datas["outcomes"][str(odd)]["code"]
                team_odd = datas["odds"][str(odd)]
                if team_code == "1":
                    item["odd_home"] = team_odd

                elif team_code == "2":
                    item["odd_away"] = team_odd

                elif team_code.upper() == "X":
                    item["odd_draw"] = team_odd

                else:
                    raise Warning('\033[31m' + bet_id + ": isn't a match because code is " + team_code + " and not 1, 2 or X" + '\033[0m')
                    #Show the error and stop the process so that Pipeline doesnt try to add the datas to the db

            yield item

    def turn_to_json(self, response):
        """
        When a request is made, the datas are hard coded in the javascript of the html page.
        To make it easier to parse, the javascript and the datas needed are turned into json.
        """
        begining = re.search('PRELOADED_STATE = {', response.text).end() - 1
        end = re.search('};var BETTING_CONFIGURATION', response.text).start() + 1
        datas = json.loads(response.text[begining:end])
        #All the informations abouts bets and odds that we need are between the brackets that
        #we search for using regular expressions. They are organized in a json format.
        return datas