# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from javascrap.items import MatchItem
import json


class WinamaxrugbySpider(scrapy.Spider):
    name = 'winamaxRugby'
    allowed_domains = ['web']
    start_urls = ['https://www.winamax.fr/paris-sportifs/sports/12']

    def parse(self, response):
        item = MatchItem()
        datas = response.xpath('//script//text()').getall()
        datas = "".join(datas)
        begining = datas.find('PRELOADED_STATE = ') + 18
        end = datas.find('var BETTING_CONFIGURATION') - 1
        datas = json.loads(datas[begining:end])
        rugby = datas["sports"]["12"]
        for identification_number in rugby["matches"]:
            id_string = str(identification_number)
            if "tvChannels" in datas["matches"][id_string]:
                item["home"] = datas["matches"][id_string]["competitor1Name"]
                item["away"] = datas["matches"][id_string]["competitor2Name"]
                item["time"] = str(datetime.now())
                item["broadcasters"] = datas["matches"][id_string]["tvChannels"] 
                #(voir situation avec plusieurs diffuseurs)
                item["sport"] = "Rugby"
                item["url"] = response.url
                item["site"] = "Winamax"

                league_id = str(datas["matches"][id_string]["tournamentId"])
                item["league"] = datas["tournaments"][league_id]["tournamentName"]

                bet_id = str(datas["matches"][id_string]["mainBetId"])
                bets_odds = datas["bets"][bet_id]["outcomes"]
                for odd in range(len(bets_odds)):
                    if odd == 0:
                        item["odd_home"] = datas["odds"][str(bets_odds[odd])]
                    elif odd == 1:
                        item["odd_draw"] = datas["odds"][str(bets_odds[odd])]
                    elif odd == 2:
                        item["odd_away"] = datas["odds"][str(bets_odds[odd])]

        return item