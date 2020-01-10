# -*- coding: utf-8 -*-
import scrapy
import json
import time
from javascrap.items import MatchItem
from datetime import datetime

class ParionssportSpider(scrapy.Spider):
    name = 'parionsSportScraping'
    allowed_domains = ['web']
    download_delay = 2.0

    def start_requests(self):
        self.start_time = time.time()
        football = ['p1555879','p22892','p22893','p22895','p22894','p22950','p22951','p22953','p22954','p22957','p22958','p22959','p71501','p22962','p22963','p22965','p22968','p22969','p22970','p22906','p33559','p265446','p80118','p22926','p22927','p22928','p22929','p1329846','p1329847','p740955','p22972','p58373992','p739665','p739666','p1574760','p1574763','p58371118','p58371119','p23048','p23051','p87835','p23061','p23075','p23080','p38806','p38803','p85875','p1258375','p23098','p39380','p23105','p23110','p23111','p23112','p39260','p23132','p23137']
        rugby = ['p23211','p25819','p1126766','p31802','p1061975','p1061976','p932019','p1053770','p1061982','p1060766','p1054627','p1490764','p23229','p1336053','p58254396','p58353570']
        tennis = ['p58194873','p58367667','p58367669','p1632493,','p26370804','p58084423','p58086783','p58108668','p58194836','p58194829','p58194868','p58194869','p26363128','p58084564','p58086785','p58108610']
        basket = ['p23189','p1542534','p23152','p280118','p1502660','p110369','p1528944','p23195','p1551127','p1621976','p23206','p361616','p23199','p1614079','p536659','p23203','p1312506','p47589','p82438']
        sports = [football, tennis, basket, rugby]
        headers =  {"X-LVS-HSToken" : "hIe1k7-Q3V-irF4VwYDAwI09GAu0k3oCNB3MlIisnjeky4qofJMNXiNhs4gJDUhB43oIG5wNhT4Gx9f-8NOJW2lhogL5tfhkNIAYfrSPcSfqgHZAZDoG9sG1yWFkGbJdRnBwd2EtcJnoPu3T32oC6Q=="
    
        }
        for sport_urls in sports:
            for page in sport_urls:
                yield scrapy.http.Request('https://www.enligne.parionssport.fdj.fr/lvs-api/next/50/' + page, headers=headers, callback=self.parse)

    def parse(self, response):
        item = MatchItem()
        datas = json.loads(response.body)
        betting_infos = datas["items"]
        odds_parsed = []

        for element_id in betting_infos:
            if element_id[0] == "o" and element_id not in odds_parsed:
                m_key = betting_infos[element_id]["parent"]
                m_key_datas = betting_infos[m_key]
                if m_key_datas["desc"] not in ["1 N 2", "Face à Face"] :
                    continue
                else:
                    item["odd_draw"] = None
                    item["away"] = None
                    e_key = m_key_datas["parent"]
                    e_key_datas = betting_infos[e_key]
                    for element_id in betting_infos:
                        if element_id[0] == "o" and betting_infos[element_id]["parent"] == m_key:
                            odds_parsed.append(element_id)
                            o_key_datas = betting_infos[element_id]
                            if o_key_datas["pos"] == 1:
                                item["home"] = o_key_datas["desc"]
                                item["odd_home"] = o_key_datas["price"].replace(",",".")
                            elif o_key_datas["pos"] == 2 and e_key_datas["path"]["Sport"] in ["Football", "Basketball", "Rugby"]:
                                item["odd_draw"] = o_key_datas["price"].replace(",",".")
                            elif o_key_datas["pos"] == 2 and e_key_datas["path"]["Sport"] == "Tennis":
                                item["away"] = o_key_datas["desc"]
                                item["odd_away"] = o_key_datas["price"].replace(",",".")
                            elif o_key_datas["pos"] == 3:
                                item["away"] = o_key_datas["desc"]
                                item["odd_away"] = o_key_datas["price"].replace(",",".")

                    item["broadcasters"] = e_key_datas["tvChannel"]
                    item["sport"] = e_key_datas["path"]["Sport"]
                    item["league"] = e_key_datas["path"]["League"]
                    item["region"] = e_key_datas["path"]["Category"]
                    item["bookmaker"] = "Parions Sport"
                    item["url"] = response.url
                    item["time_scraped"] = datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')
                    date_infos = e_key_datas["start"]
                    item["playing_time"] = "20" + date_infos[0:2] + "-" + date_infos[2:4] + "-" + date_infos[4:6] + " " + date_infos[6:8] + ":" + date_infos[8:10]


                    yield item