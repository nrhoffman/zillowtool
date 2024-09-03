import pandas as pd
import psycopg2
from psycopg2.extensions import AsIs
import psycopg2.extras

class Connection():
    def __init__(self, config, create_tables):
        self.config = config
        if create_tables == True:
            self.createtables()

    def connectdb(self):
        conn = psycopg2.connect(database = self.config["DATABASE"]["Database"], 
                        user = self.config["DATABASE"]["UserName"], 
                        host= self.config["DATABASE"]["Host"],
                        password = self.config["DATABASE"]["Password"],
                        port = self.config["DATABASE"]["Port"])
        return conn
    
    def createtables(self):
        connect = self.connectdb()
        cur = connect.cursor()
        self.droptables(cur)
        cur.execute("""CREATE TABLE homesforsale(
                    region VARCHAR(50) PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    value DOUBLE PRECISION);
                    """)
        cur.execute("""CREATE TABLE homesthatsold(
                    region VARCHAR(50) PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    value DOUBLE PRECISION);
                    """)
        cur.execute("""CREATE TABLE meandayspending(
                    region VARCHAR(50) PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    value DOUBLE PRECISION);
                    """)
        cur.execute("""CREATE TABLE meanpricecut(
                    region VARCHAR(50) PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    date VARCHAR(50) NOT NULL,
                    value DOUBLE PRECISION);
                    """)
        connect.commit()
        cur.close()
        connect.close()

    def droptables(self, cur):
        cur.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            cur.execute("""DROP table IF EXISTS """ + table[0])
    
    def getrowcount(self, table):
        connect = self.connectdb()
        cur = connect.cursor()
        query = "SELECT COUNT(*) FROM " + table
        cur.execute(query)
        count = cur.fetchall()
        cur.close()
        connect.close()
        return count[0]
    
    def insertdata(self, table, region, city, state, date, value):
        connect = self.connectdb()
        cur = connect.cursor()
        cur.execute("""INSERT INTO %s(Region, City, State, Date, Value) VALUES(%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING""",
                    (AsIs(table), region, city, state, date, value))
        connect.commit()
        cur.close()
        connect.close()

    def getstates(self):
        connect = self.connectdb()
        cur = connect.cursor()
        query = "SELECT DISTINCT state FROM meanpricecut"
        cur.execute(query)
        list = cur.fetchall()
        state_list = [state[0] for state in list]
        cur.close()
        connect.close()
        return sorted(state_list)
    
    def getcities(self, state):
        connect = self.connectdb()
        cur = connect.cursor()
        query = "SELECT DISTINCT city FROM meanpricecut WHERE state = '"+state+"'"
        cur.execute(query)
        list = cur.fetchall()
        city_list = [city[0] for city in list]
        cur.close()
        connect.close()
        return sorted(city_list)

    def getdata(self, state, city):
        connect = self.connectdb()
        cur = connect.cursor()
        cur.execute("""SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        list = cur.fetchall()
        cur.close()
        cur = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
        df = pd.DataFrame()
        for table in list:
            cur.execute("SELECT * FROM %s WHERE state = %s AND city = %s", (AsIs(table[0]), state, city))
            query = cur.fetchall()
            query = pd.DataFrame.from_dict(query)
            query["type"] = table[0]
            df = pd.concat([df, query], ignore_index=True)
        df['date'] = pd.to_datetime(df['date'])
        cur.close()
        connect.close()
        return df
