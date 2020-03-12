from flask import Flask, send_file
from flask import request, jsonify, abort
from passlib.apps import custom_app_context as pwd_context
import pymysql
from datetime import datetime

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                     user='rayane',
                     password='i77EWEsN',
                     db='BookMarket',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@app.route('/download')
def return_kivy_file():
    try:
        return send_file('apk/main__armeabi-v7a-0.1-armeabi-v7a-debug.apk', attachment_filename='freebet.apk')
    except FileNotFoundError:
        abort(404)

@app.route('/sports', methods=['GET'])
def sports():
    """
    When appurl/sports is requested, all the sports of the Database or sent in a jsonformat containing
    the name of the sport and the associated id
    """
    cursor.execute("SELECT nom, id FROM sport")
    rows = cursor.fetchall()
    return jsonify(sports=rows)

@app.route('/<sport_id>/regions', methods=['GET'])
def regions(sport_id):
    """
    When appurl/<int:sport_id>/regions is requested, depending of the number used in sport_id
    parameter, the regions names related to the sport which match this id will be sent in a json format
    """
    if "matches_available" in request.args:
        parameters = bool(request.args["matches_available"])
    else:
        parameters = None
    #Check if the user wants to return regions that have bets available or every single region

    if parameters == True:
        cursor.execute("SELECT DISTINCT region FROM rencontre WHERE sport_id=%s AND CURRENT_TIMESTAMP() <= date_affrontement", sport_id)
    else:
        if sport_id == 0:
            cursor.execute("SELECT DISTINCT region FROM rencontre")
        else:
            cursor.execute("SELECT DISTINCT region FROM rencontre WHERE sport_id=%s", sport_id)
    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["region"])
    return jsonify(regions=datas)

@app.route('/<sport_id>/competitions', methods=['GET'])
def competitions(sport_id):
    """
    When appurl/<int:sport_id>/competitions is called , it returns competitions related to the regions used as parameters.
    If no region in parameters, return all competitions if sport_id set to 0, or competitions related to the sport_id selected if exist.
    """
    parameters = request.args.getlist("region")

    if parameters:
        sql = "SELECT DISTINCT competition FROM rencontre WHERE sport_id=%s AND region IN ("
        for parameter in parameters:
            if parameter != parameters[-1]:
                sql += "\"" + parameter + "\","
            else:
                sql += "\"" + parameter + "\")"
        cursor.execute(sql, sport_id)
    else:
        if sport_id == 0:
            cursor.execute("SELECT DISTINCT competition FROM rencontre")
        else:
            cursor.execute("SELECT DISTINCT competition FROM rencontre WHERE sport_id=%s", (sport_id))
    #If the url is requested with region arguments return the competitions of those regions, otherwise return all the competitions for a sport

    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["competition"])
    return jsonify(competitions=datas)


@app.route('/<int:sport_id>/rencontres', methods=['GET'])
def rencontre(sport_id):
    """
    When appurl/<int:sport_id>/rencontres is called, returns matches related to the competitions used as parameters.
    If no competition in parameters, return all matches if sport_id set to 0, or matches related to the sport_id selected if exist.
    """
    parameters = request.args.getlist("competition")
    #Return matches for the selected comeptitions
    private = bool(request.args.getlist("private"))
    #If private is set to True in the url argument private, return bet that have been created by users, otherwise return matches scraped from Winamax
    if private == True:
        cursor.execute("SELECT * FROM rencontre WHERE utilisateur_id AND CURRENT_TIMESTAMP() <= date_affrontement AND mise_maximale > 0 ORDER BY date_affrontement")
    else:
        if parameters:
            cursor.execute("SELECT MAX(date_scraping) FROM rencontre")
            last_scrap = cursor.fetchone()["MAX(date_scraping)"]
            sql = "SELECT * FROM rencontre WHERE date_scraping=%s\
                        AND utilisateur_id IS NULL\
                        AND sport_id = %s\
                        AND CURRENT_TIMESTAMP() <= date_affrontement \
                        AND competition IN ("
            for parameter in parameters:
                if parameter != parameters[-1]:
                    sql += "\"" + parameter + "\","
                else:
                    sql += "\"" + parameter + "\")"
            sql += " ORDER BY date_affrontement"
            cursor.execute(sql, (last_scrap, sport_id))
            """
            This sql select matches from the last scrap that haven't been created by any user, haven't been played yet and are contained in
            the competitions defined in the url arguments
            """
        else:
            if sport_id == 0:
                cursor.execute("SELECT * FROM rencontre")
            else:
                cursor.execute("SELECT * FROM rencontre WHERE sport_id=%s", (sport_id))


    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append({"id": str(row["id"]),"id_match":row["match_reference"], "sport": row["sport_id"], "region": row["region"], "competition": row["competition"],"date" : row["date_affrontement"],\
                      "cote_nul" : str(row["cote_match_nul"]),"domicile" : row["equipe_domicile"], "cote_dom" :str(row["cote_domicile"]), "exterieur" : row["equipe_exterieure"], "cote_ext" : str(row["cote_exterieure"]), \
                      "date_scraping": row["date_scraping"],"resultat_id": row["resultat_id"],"utilisateur_id":row["utilisateur_id"], "mise": row["mise_maximale"], "tv" : row["diffuseur"]})
    return jsonify(matches=datas, amount=len(rows))

@app.route('/register', methods = ['POST'])
def create_new_user():
    """
    Check if the user exist before creating a new if he doesn't
    """
    username = request.json.get('username')
    password = request.json.get('password')

    cursor.execute("SELECT nom FROM utilisateur WHERE nom=%s", username)
    user_exist = cursor.fetchone()
    if user_exist is not None:
        return jsonify({ "error_message": "Utilisateur déjà existant" }), 400
    password_hash = pwd_context.encrypt(password)
    cursor.execute("INSERT INTO utilisateur (nom, mot_de_passe, argent) VALUES (%s, %s, 1000)", (username, password_hash))
    connection.commit()
    return jsonify({ "succes_message": "L'utilisateur a bien été ajouté" }), 201

@app.route('/login', methods = ['POST'])
def login():
    """
    Check the user already exist and send back to the app the necessary informations so the user can use the kivy app
    """
    username = request.json.get('username')
    password = request.json.get('password')

    cursor.execute("SELECT id, mot_de_passe, argent  FROM utilisateur WHERE nom=%s", username)
    user_exist = cursor.fetchone()
    if user_exist is not None:
        if pwd_context.verify(password, user_exist["mot_de_passe"]):
            return jsonify({ "succes_message": "Connexion réussie", "user_id": user_exist["id"], "money": user_exist["argent"]}), 201
        else:
            return jsonify({ "error_message": "Mauvais mot de passe" }), 400
    else:
        return jsonify({ "error_message": "Cet utilisateur n'existe pas" }), 400

@app.route('/bet', methods = ['POST'])
def bet():
    """
    If the match hasn't begin yet, save the bet made by the user in database
    """
    match_id = request.json.get("match_id")
    user_id = request.json.get("user_id")
    team_selected = request.json.get("team_selected")
    odd = float(request.json.get("odd"))
    bet = request.json.get("bet")
    private = request.json.get("private")
    cursor.execute("SELECT date_affrontement  FROM rencontre WHERE id=%s", match_id)
    date_match = cursor.fetchone()
    if datetime.now() >=  date_match["date_affrontement"]:
        return jsonify({ "error_message": "Match commencé.Paris indisponible." }), 400
    else:
        if private:
            cursor.execute("UPDATE rencontre SET mise_maximale = mise_maximale - %s WHERE id=%s",(bet, match_id))
        cursor.execute("INSERT INTO paris (rencontre_id, utilisateur_id, mise, equipe_pariee, cote) VALUES (%s, %s, %s, %s, %s)", (match_id, user_id, bet, team_selected, odd))
        cursor.execute("UPDATE utilisateur SET argent = argent - %s WHERE id=%s",(bet, user_id))
        connection.commit()
        return jsonify({ "succes_message": "Pari enregistré", "bet": bet }), 201

@app.route('/betexchange', methods = ['POST'])
def save_user_bet():
    """
    If the match hasn't begin yet, save the match created by the user.This match can then be bet on by other user.
    """
    match_id = request.json.get("match_id")
    user_id = request.json.get("user_id")
    team_selected = request.json.get("team_selected")
    odd = float(request.json.get("odd"))
    bet = request.json.get("bet")
    cursor.execute("SELECT date_affrontement  FROM rencontre WHERE id=%s", match_id)
    date_match = cursor.fetchone()
    if datetime.now() >=  date_match["date_affrontement"]:
        return jsonify({ "error_message": "Match commencé.Paris indisponible." }), 400
    else:
        odd_home = None if team_selected != 1 else odd
        odd_draw = None if team_selected != 2 else odd
        odd_away = None if team_selected != 3 else odd
        cursor.execute("INSERT INTO rencontre (competition, cote_match_nul, equipe_domicile, cote_domicile, equipe_exterieure, cote_exterieure, sport_id, \
                        diffuseur, region, date_affrontement, date_scraping, bookmaker_id, match_reference, resultat_id, utilisateur_id, mise_maximale)\
                        (SELECT competition, %s, equipe_domicile, %s, equipe_exterieure, %s, sport_id, diffuseur, region, date_affrontement, NULL, bookmaker_id,\
                        match_reference, resultat_id, %s, %s  FROM rencontre WHERE id=%s)",
                        (odd_draw, odd_home, odd_away, user_id, bet, match_id))
        cursor.execute("UPDATE utilisateur SET argent = argent - %s WHERE id=%s",(bet*odd, user_id))
        connection.commit()
        return jsonify({ "succes_message": "Pari enregistré", "bet": bet }), 201

@app.route('/<user_id>/bets', methods = ['GET'])
def get_user_bets(user_id):
    """
    Return bets made by a user depending of his id
    """
    cursor.execute("SELECT * FROM paris WHERE utilisateur_id=%s ORDER BY date_enregistrement DESC", user_id)
    bets = cursor.fetchall()
    for bet in bets:
        bet["cote"] = str(bet["cote"])
        cursor.execute("SELECT equipe_domicile, equipe_exterieure, resultat_id, date_affrontement, competition FROM rencontre WHERE id=%s", bet["rencontre_id"])
        match_infos = cursor.fetchone()
        bet["match_infos"] = match_infos
    return jsonify(bets=bets)

@app.route('/winners', methods = ['GET'])
def user_bets():
    """
    Request the three players who have won the most money.
    """
    cursor.execute("SELECT nom, argent FROM utilisateur ORDER BY argent DESC LIMIT 3")
    winners = cursor.fetchall()
    return jsonify(winners=winners)

if __name__ == "__main__":
    app.run()
