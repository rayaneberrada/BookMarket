from flask import Flask
from flask import request, jsonify
import pymysql


app = Flask(__name__)

class User():
    # ...

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


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
    sport_id = cursor.execute("SELECT id FROM sport WHERE nom=%s", sport_name)
    cursor.execute("SELECT DISTINCT region FROM rencontre WHERE sport_id=%s", sport_id)
    rows = cursor.fetchall()
    datas = []
    for row in rows:
        datas.append(row["region"])
    return jsonify(regions=datas)

@app.route('/rencontres/competitions', methods=['GET'])
def match():
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
        datas.append({"cote_nul" : str(row["cote_match_nul"]),"domicile" : row["equipe_domicile"], "cote_dom" :str(row["cote_domicile"]),\
                    "exterieur" : row["equipe_exterieure"], "cote_ext" : str(row["cote_exterieure"]), "date" : row["date_affrontement"],\
                    "tv" : row["diffuseur"]})
        #Voir si on garde les cotes au format string car jsonify n'accepte pas les decimal
    return jsonify(matches=datas)

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

if __name__ == "__main__":
    app.run()