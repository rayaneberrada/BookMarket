# -*- coding: utf-8 -*-
import scrapy, json, re, datetime, time
from javascrap.items import MatchItem
from urllib.parse import urljoin



class WinamaxrugbySpider(scrapy.Spider):
    name = 'winamaxFootballScraping'
    allowed_domains = ['web']
    download_delay = 2.0
    start_urls = ['https://www.winamax.fr/paris-sportifs/sports']

    def parse(self, response):
        """
        The parsing function will go through the html page donwloaded and extrat informations
        we are interested in
        """
        datas = self.turn_to_json(response)

        for sport in datas["sports"]:
            if datas["sports"][str(sport)]["sportName"] == "Football":
                #We define here which sport we are going to scrap
                sport_id = str(sport)

        regions = datas["sports"]["1"]["categories"]        
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
                                             cb_kwargs=dict(competition=str(competition_id), region=region_name),\
                                             dont_filter=True,
                                             headers={"User-Agent":"berradarayane@gmail.com"})

    def parse_matches(self, response, competition, region):
        item = MatchItem()
        datas = self.turn_to_json(response)
        matches = datas["tournaments"][competition]["matches"]
        for match_id in matches:
            match_datas = datas["matches"][str(match_id)]
            item["home"] = match_datas["competitor1Name"]
            item["away"] = match_datas["competitor2Name"]
            item["region"] = region
            item["time_scraped"] = time.time()

            if "tvChannels" in match_datas:
                item["broadcasters"] = match_datas["tvChannels"] 
                #(voir situation avec plusieurs diffuseurs)
            else:
                item["broadcasters"] = None

            item["sport"] = "Football"
            item["url"] = response.url
            item["bookmaker"] = "Winamax"
            item["league"] = datas["tournaments"][competition]["tournamentName"]
            item["playing_time"] = datetime.datetime.fromtimestamp(match_datas["matchStart"]).strftime('%Y-%m-%d %H:%M:%S')

            #Améliorer l'affichage de la date

            bet_id = str(match_datas["mainBetId"])
            odds_id = datas["bets"][bet_id]["outcomes"]
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
                    raise Warning(bet_id + ": isn't a match because code is " + team_code + " and not 1, 2 or X")

            yield item

    def turn_to_json(self, response):
        datas = response.xpath('//script//text()').getall()
        #All the necessary datas are inside the script tags of the html
        datas = "".join(datas)
        begining = re.search('PRELOADED_STATE = {', datas).end() - 1
        end = re.search('};var BETTING_CONFIGURATION', datas).start() + 1
        datas = json.loads(datas[begining:end])
        #All the informations abouts bets and odds that we need are between the brackets that
        #we search for using regular expressions. They are organized in a json format.
        return datas