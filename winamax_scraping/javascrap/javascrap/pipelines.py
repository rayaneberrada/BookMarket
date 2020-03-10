# -*- coding: utf-8 -*-
import pymysql.cursors
import datetime
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
            # winamaxResultsScraping scrap yesterday results
            cursor.execute("SELECT * FROM rencontre WHERE match_reference=%s", item["reference"])
            matches = cursor.fetchall()
            for match in matches:
                cursor.execute("SELECT resultat_id FROM rencontre WHERE id=%s", match["id"])
                current_result = cursor.fetchone()["resultat_id"]
                # can help for debugging: print(match["id"], current_result, item["result"])

                if current_result == None:
                    result = 1 if item["result"] == "home" else 2 if item["result"] == "away" else 3
                    params = (result, match["id"])
                    cursor.execute("UPDATE rencontre SET resultat_id=%s WHERE id=%s", params)

                    cursor.execute("SELECT * FROM paris WHERE rencontre_id=%s", match["id"])
                    bets = cursor.fetchall()
                    for bet in bets:
                        if bet["verifie"] != 1:
                            #We get all the bets that haven't been checked for their result yet
                            if bet["result_id"] == result:
                                winning = int(bet["mise"]*bet["cote"])
                                cursor.execute("UPDATE utilisateur SET argent = argent + %s WHERE id=%s", (winning, bet["utilisateur_id"]))
                                #If the result set in the bet is the same as the result of the match, we set a value for winning
                            elif bet["result_id"] != result and match["utilisateur_id"]:
                            #If the match and bet result don't match, and it's a bet created by a user
                                winning = int(bet["mise"]*bet["cote"] + bet["mise"] + match["mise_maximale"]*bet["cote"])
                                """
                                When the user create a bet, the amount that the user can lose is deducted from his money(maximum bet set by user times
                                odd set by user). Exemple: if max_bet = 5 and odd = 10, the user would be deducted 50
                                So when a player don't win a bet create by the user, the user needs to be refund for the amount bet by the player
                                times the odd of the bet, plus the bet of the player (that is the actual benefit the user who created the bet make, the
                                rest is only refund for the money blocked) and the amount nobody bet on times the odd.
                                """
                                cursor.execute("UPDATE utilisateur SET argent = argent + %s WHERE id=%s", (winning, match["utilisateur_id"]))
                            cursor.execute("UPDATE paris SET verifie=1 WHERE id=%s", bet["id"])


            yesterday = (datetime.datetime.now() - datetime.timedelta(hours=28)).strftime('%Y-%m-%d %H:%M')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            cursor.execute("SELECT * FROM rencontre WHERE date_affrontement BETWEEN %s AND %s", (yesterday,now))
            matches = cursor.fetchall()
            for match in matches:
                #For yesterday matches
                if match["mise_maximale"] > 0:
                    odd = match["cote_domicile"] if match["equi_domicile"] else match["cote_exterieure"] if match["equipe_exterieure"] else match["cote_match_nul"]
                    refund = match["mise_maximale"]*odd
                    cursor.execute("UPDATE utilisateur SET argent = argent + %s WHERE id=%s", (refund, match["utilisateur_id"]))
                    #If the the amount set to bet by the creator of the bet is not empty, refund the creator of what is left
                if not match["resultat_id"]:
                    #If a match stil doesn't have a result, refund the users who bets on this match
                    cursor.execute("SELECT * FROM paris WHERE rencontre_id=%s", match["id"])
                    bets = cursor.fetchall()
                    for bet in bets:
                        if bet["verifie"] != 1:
                            continue
                        else:
                            refund = bet["mise"]
                            cursor.execute("UPDATE utilisateur SET argent = argent + %s WHERE id=%s", (refund, match["utilisateur_id"]))

        connection.commit()
