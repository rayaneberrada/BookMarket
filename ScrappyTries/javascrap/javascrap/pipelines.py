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
                                    date_affrontement, date_scraping, match_reference)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            params = (item["league"], item["odd_draw"], item["home"],\
                    item["odd_home"], item["away"], item["odd_away"],\
                    sport, item["broadcasters"], item["region"], bookmaker,\
                    item["playing_time"], item["time_scraped"], item["reference"])
            cursor.execute(sql, params)

        elif spider.name == 'winamaxResultsScraping':
            cursor.execute("SELECT id FROM rencontre WHERE match_reference=%s", item["reference"])
            matches = cursor.fetchall()
            raise Warning(matches)
            for match in matches:
                if match["id"] == None:
                    return None
                else:
                    cursor.execute("SELECT resultat_id FROM rencontre WHERE id=%s", match["id"])
                    current_result = cursor.fetchone()
                    if current_result == None:
                        result = "Domicile" if item["result"] == "home" else "Exterieur" if item["result"] == "away" else "Nul"
                        cursor.execute("SELECT id FROM resultat WHERE statut=%s", result)
                        result_id = cursor.fetchone()["id"]
                        params = (result_id, match["id"])
                        cursor.execute("UPDATE rencontre SET resultat_id=%s WHERE id=%s", params)
                        cursor.execute("SELECT * FROM paris WHERE rencontre_id=%s", match["id"])
                        bets = cursor.fetchall()
                        for bet in bets:
                            if bet["result_id"] == result_id:
                                winning = bet["mise"]*bet["cote"]
                                cursor.execute("UPDATE utilisateur SET argent = argent + %s WHERE id=%s", (winning, bet["utilisateur_id"]))
                                cursor.execute("UPDATE paris SET verifie=1 WHERE id=%s", bet["id"])


        
        connection.commit()

        #Uncomment return item can help for debugging
        #return item