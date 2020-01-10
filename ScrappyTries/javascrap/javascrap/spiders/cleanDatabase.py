import pymysql

class CLeaner:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='rayane',
                             password='i77EWEsN',
                             db='BookMarket',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def clean(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP DATABASE BookMarket")
        cursor.execute("CREATE DATABASE BookMarket")
        cursor.execute("use BookMarket")
        stmts = self.parse_sql("tableCreation.sql")
        for stmt in stmts:
            cursor.execute(stmt)
        cursor.execute("INSERT INTO sport (nom) VALUES ('Football'),('Rugby'),('Basketball'), ('Tennis')")
        cursor.execute("INSERT INTO bookmaker (nom) VALUES ('Winamax'),('Parions Sport')")
        self.connection.commit()

    def parse_sql(self, filename):
        data = open(filename, 'r').readlines()
        stmts = []
        DELIMITER = ';'
        stmt = ''

        for lineno, line in enumerate(data):
            if not line.strip():
                continue

            if line.startswith('--'):
                continue

            if 'DELIMITER' in line:
                DELIMITER = line.split()[1]
                continue

            if (DELIMITER not in line):
                stmt += line.replace(DELIMITER, ';')
                continue

            if stmt:
                stmt += line
                stmts.append(stmt.strip())
                stmt = ''
            else:
                stmts.append(line.strip())
        return stmts

C = CLeaner()
C.clean()