from flask import Flask
from flask import request, jsonify
import pymysql

app = Flask(__name__)

@app.route('/sports', methods=['GET'])
def sports():
    """
    When appurl/sports is requested, all the sports of the Database or sent in a jsonformat containing
    the name of the sport and the associated id
    """
    connection = pymysql.connect(host='localhost',
                     user='rayane',
                     password='i77EWEsN',
                     db='BookMarket',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    cursor.execute("SELECT nom, id FROM sport")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/rencontres/<int:sport_id>/regions', methods=['GET'])
def regions(sport_id):
    """
    When appurl/rencontres/<int:sport_id>/regions is requested, depending of the number used in sport_id
    parameter, the regions names related to the sport which match this id will be sent in a json format
    """
    connection = pymysql.connect(host='localhost',
                     user='rayane',
                     password='i77EWEsN',
                     db='BookMarket',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

    parameters = request.args
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT region FROM rencontre WHERE sport_id=%s", sport_id)
    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["region"])
    return jsonify(region=datas)

@app.route('/rencontres/competition', methods=['GET'])
def competition():
    connection = pymysql.connect(host='localhost',
                     user='rayane',
                     password='i77EWEsN',
                     db='BookMarket',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    parameters = request.args.getlist("region")

    if parameters:
        sql = "SELECT DISTINCT competition FROM rencontre WHERE region IN ("
        for parameter in parameters:
            if parameter != parameters[-1]:
                sql += "'" + parameter + "',"
            else:
                sql += "'" + parameter + "')"
        cursor.execute(sql)
    else:
        cursor.execute("SELECT DISTINCT competition FROM rencontre")

    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["competition"])
    return jsonify(competitions=datas)
    

@app.route('/rencontres', methods=['GET'])
def rencontre():
    connection = pymysql.connect(host='localhost',
                     user='rayane',
                     password='i77EWEsN',
                     db='BookMarket',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    parameters = request.args.getlist("competition")

    if parameters:
        sql = "SELECT cote_match_nul, equipe_domicile,cote_domicile, equipe_exterieure,\
                     cote_exterieure,date_affrontement,diffuseur FROM rencontre WHERE competition IN ("
        for parameter in parameters:
            if parameter != parameters[-1]:
                sql += "'" + parameter + "',"
            else:
                sql += "'" + parameter + "')"
        cursor.execute(sql)
    else:
        cursor.execute("SELECT cote_match_nul, equipe_domicile,cote_domicile, equipe_exterieure,\
                     cote_exterieure,date_affrontement,diffuseur FROM rencontre")

    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append([str(row["cote_match_nul"]),row["equipe_domicile"], str(row["cote_domicile"]),\
                    row["equipe_exterieure"], str(row["cote_exterieure"]), row["date_affrontement"],\
                    row["diffuseur"]])
        #Voir si on garde les cotes au format string car jsonify n'accepte pas les decimal
    return jsonify(matches=datas)

if __name__ == "__main__":
    app.run()