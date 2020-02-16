from flask import Flask
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

@app.route('/sports', methods=['GET'])
def sports():
    """
    When appurl/sports is requested, all the sports of the Database or sent in a jsonformat containing
    the name of the sport and the associated id
    """
    cursor = connection.cursor()
    cursor.execute("SELECT nom, id FROM sport")
    rows = cursor.fetchall()
    return jsonify(sports=rows)

@app.route('/rencontres/<sport_name>/regions', methods=['GET'])
def regions(sport_name):
    """
    When appurl/rencontres/<int:sport_id>/regions is requested, depending of the number used in sport_id
    parameter, the regions names related to the sport which match this id will be sent in a json format
    """
    parameters = request.args
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM sport WHERE nom=%s", sport_name)
    sport_id = cursor.fetchone()["id"]
    print(sport_name,sport_id)
    cursor.execute("SELECT DISTINCT region FROM rencontre WHERE sport_id=%s", sport_id)
    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["region"])
    return jsonify(regions=datas)

@app.route('/rencontres/<sport_name>/competitions', methods=['GET'])
def competitions(sport_name):
    cursor = connection.cursor()
    parameters = request.args.getlist("region")
    cursor.execute("SELECT id FROM sport WHERE nom=%s", sport_name)
    sport_id = cursor.fetchone()["id"]

    if parameters:
        sql = "SELECT DISTINCT competition FROM rencontre WHERE sport_id=%s AND region IN ("
        for parameter in parameters:
            if parameter != parameters[-1]:
                sql += "\"" + parameter + "\","
            else:
                sql += "\"" + parameter + "\")"
        cursor.execute(sql, sport_id)
    else:
        cursor.execute("SELECT DISTINCT competition FROM rencontre")

    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["competition"])
    return jsonify(competitions=datas)
    

@app.route('/rencontres', methods=['GET'])
def rencontre():
    cursor = connection.cursor()
    parameters = request.args.getlist("competition")

    if parameters:
        cursor.execute("SELECT MAX(date_scraping) FROM rencontre")
        last_scrap = cursor.fetchone()["MAX(date_scraping)"]
        sql = "SELECT id, cote_match_nul, equipe_domicile,cote_domicile, equipe_exterieure,\
                     cote_exterieure,date_affrontement,diffuseur,competition FROM rencontre WHERE date_scraping=%s\
                     AND CURDATE() <= date_affrontement \
                     AND competition IN ("
        for parameter in parameters:
            if parameter != parameters[-1]:
                sql += "\"" + parameter + "\","
            else:
                sql += "\"" + parameter + "\")"
        sql += " ORDER BY date_affrontement"
        cursor.execute(sql, last_scrap)
    else:
        cursor.execute("SELECT id, cote_match_nul, equipe_domicile,cote_domicile, equipe_exterieure,\
                     cote_exterieure,date_affrontement,diffuseur,competition FROM rencontre ORDER BY date_affrontement")

    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append({"cote_nul" : str(row["cote_match_nul"]),"domicile" : row["equipe_domicile"], "cote_dom" :str(row["cote_domicile"]),\
                    "exterieur" : row["equipe_exterieure"], "cote_ext" : str(row["cote_exterieure"]), "date" : row["date_affrontement"],\
                    "tv" : row["diffuseur"], "id": str(row["id"]), "competition": row["competition"]})
        #Voir si on garde les cotes au format string car jsonify n'accepte pas les decimal
    return jsonify(matches=datas)

@app.route('/users', methods = ['POST'])
def new_user():
    cursor = connection.cursor()
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
    cursor = connection.cursor()
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

@app.route('/bets', methods = ['POST'])
def bet():
    cursor = connection.cursor()
    match_id = request.json.get("match_id")
    user_id = request.json.get("user_id")
    team_selected = request.json.get("team_selected")
    odd = float(request.json.get("odd"))
    bet = request.json.get("bet")
    cursor.execute("SELECT date_affrontement  FROM rencontre WHERE id=%s", match_id)
    date_match = cursor.fetchone()
    print(date_match)
    if datetime.now() >=  date_match["date_affrontement"]:
        return jsonify({ "error_message": "Match commencé.Paris indisponible." }), 400
    else:
        cursor.execute("INSERT INTO paris (rencontre_id, utilisateur_id, mise, equipe_pariee, cote) VALUES (%s, %s, %s, %s, %s)", (match_id, user_id, bet, team_selected, odd))
        cursor.execute("UPDATE utilisateur SET argent = argent - %s WHERE id=%s",(bet, user_id))
        connection.commit()
        return jsonify({ "succes_message": "Pari enregistré", "bet": bet }), 201
    #Vérifier qu'une cote existe

@app.route('/<user_id>/bets', methods = ['GET'])
def get_user_bets(user_id):
    cursor = connection.cursor()
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
    cursor = connection.cursor()
    cursor.execute("SELECT nom, argent FROM utilisateur ORDER BY argent DESC LIMIT 3")
    winners = cursor.fetchall()
    return jsonify(winners=winners)

if __name__ == "__main__":
    app.run()