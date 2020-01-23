# -*- coding: utf-8 -*-
import pymysql.cursors
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class JavascrapPipeline(object):
    def process_item(self, item, spider):

        connection = pymysql.connect(host='localhost',
                             user='rayane',
                             password='i77EWEsN',
                             db='BookMarket',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        if spider.name == 'winamaxScraping':
            cursor.execute("SELECT id FROM sport WHERE nom=%s", item["sport"])
            sport = cursor.fetchone()["id"]

            cursor.execute("SELECT id FROM bookmaker WHERE nom=%s", item["bookmaker"])
            bookmaker = cursor.fetchone()["id"]
            sql = (
                "INSERT INTO rencontre (competition, cote_match_nul, equipe_domicile,\
                                    cote_domicile, equipe_exterieure, cote_exterieure,\
                                    sport_id, diffuseur, region, bookmaker_id,\
                                    date_affrontement, date_scraping)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            datas = (item["league"], item["odd_draw"], item["home"],\
                    item["odd_home"], item["away"], item["odd_away"],\
                    sport, item["broadcasters"], item["region"], bookmaker,\
                    item["playing_time"], item["time_scraped"])

        elif spider.name == 'winamaxResultsScraping':
            cursor.execute("SELECT id FROM rencontre WHERE equipe_domicile=%s AND equipe_exterieure=%s AND \
                date_affrontement=%s", (item["home"], item["away"], item["date"]))
            match_id = cursor.fetchone()["id"]
            result = "Domicile" if item["result"] == "home" else "Exterieur" if item["result"] == "away" else "Nul"
            cursor.execute("SELECT id FROM resultat WHERE statut=%s", result)
            result_id = cursor.fetchone()["id"]
            datas = (result_id, match_id)
            sql = ("UPDATE rencontre SET result_id=%s WHERE id=%s")

        cursor.execute(sql, datas)
        connection.commit()

        return item