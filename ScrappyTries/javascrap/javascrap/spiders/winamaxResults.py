# -*- coding: utf-8 -*-
import scrapy
import json
import time
from javascrap.items import ResultItem
from datetime import datetime, timedelta

class WinamaxResults(scrapy.Spider):
    name = 'winamaxResultsScraping'
    allowed_domains = ['web']
    download_delay = 2.0

    def start_requests(self):
        self.start_time = time.time()     
        yield scrapy.http.Request('https://lsc.fn.sportradar.com/winamaxfr/fr/Europe:Helsinki/gismo/event_fullfeed')

    def parse(self, response):
        item = ResultItem()
        reponse = json.loads(response.body)

        for sport in reponse["doc"][0]["data"]:
            if sport["name"] in ["Football", "Tennis", "Basketball", "Rugby"]:
                for country in sport["realcategories"]:
                    for tournament in country["tournaments"]:
                        for match in tournament["matches"]:
                            item["result"] = match["result"]["winner"]
                            item["home"] = match["teams"]["home"]["name"]
                            item["away"] = match["teams"]["away"]["name"]
                            minutes = int(match["_dt"]["time"][3:5])
                            hour = int(match["_dt"]["time"][0:2])
                            year = int("20" + match["_dt"]["date"][6:8])
                            month = int(match["_dt"]["date"][3:5])
                            day = int(match["_dt"]["date"][0:2])
                            date = datetime(year, month, day, hour, minutes) - timedelta(hours=1)
                            item["date"] = date.strftime('%Y-%m-%d %H:%M')
                            yield item
            else:
                continue

            