# -*- coding: utf-8 -*-
import scrapy
import json
import time
from javascrap.items import MatchItem
from datetime import datetime

class BetclicSpider(scrapy.Spider):
    name = 'betclicScraping'
    allowed_domains = ['web']
    download_delay = 2.0

    def start_requests(self):
        self.start_time = time.time() 
        # https://offer.cdn.betclic.fr/api/pub/v4/events?application=2&countrycode=fr&language=fr&limit=40&offset=0&sitecode=frfr&sortBy=ByDateAsc&sportIds=2           
        sport_ids = {"1" : "Football", "2" : "Tennis", "4" : "Basket", "5" : "Rugby"}
        for sport in sport_ids:
                yield scrapy.http.Request('https://offer.cdn.betclic.fr/api/pub/v4/events?application=2&countrycode=fr&language=fr&limit=1000&offset=0&sitecode=frfr&sortBy=ByDateAsc&sportIds=' + sport, self.parse, headers={"User-Agent":"berradarayane@gmail.com"})

    def parse(self, response):
        item = MatchItem()
        datas = json.loads(response.body)
        odds_parsed = []
        for match in datas:
            if len(match["markets"]) == 0:
                continue
            item["odd_draw"] = None
            for odd in match["markets"][0]["selections"]:
                if odd["lx"] == "1":
                    item["home"] = odd["name"]
                    item["odd_home"] = odd["odds"]
                elif odd["lx"] == "Nul":
                    item["odd_draw"] = odd["odds"]
                elif odd["lx"] == "2":
                    item["away"] = odd["name"]
                    item["odd_away"] = odd["odds"]

            item["broadcasters"] = None
            item["sport"] = match["competition"]["sport"]["name"]
            if match["competition"]["sport"]["name"] == "Basket-ball":
                item["sport"] = "Basketball"
            elif match["competition"]["sport"]["name"] == "Rugby à XV":
                item["sport"] = "Rugby"
            item["league"] = match["competition"]["name"]
            item["region"] = None
            item["bookmaker"] = "Betclic"
            item["url"] = response.url
            item["time_scraped"] = datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')
            item["playing_time"] = match["date"][:-4].replace("T", " ")

            yield item