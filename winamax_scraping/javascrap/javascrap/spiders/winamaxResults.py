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
        yield scrapy.http.Request('https://lsc.fn.sportradar.com/winamaxfr/fr/Europe:Helsinki/gismo/event_fullfeed/-1')

    def parse(self, response):
        item = ResultItem()
        reponse = json.loads(response.body)

        for sport in reponse["doc"][0]["data"]:
            if sport["name"] in ["Football", "Tennis", "Basketball", "Rugby"]:
                for country in sport["realcategories"]:
                    for tournament in country["tournaments"]:
                        for match in tournament["matches"]:
                            item["result"] = match["result"]["winner"]
                            item["reference"] = match["_id"]
                            yield item
                            # print item adding sport["name"] and match["teams"]["home"]["name"] for help for debugging
            else:
                continue

