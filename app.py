import requests
from requests.auth import HTTPDigestAuth
import sqlite3

#
#       Database Connection Class
#

class db:
    
    #Constructor calls the database to extract the miners table

    def __init__(self):
        connection = sqlite3.connect('miners.db')
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Miners
                        (IP TEXT, Username TEXT, Password TEXT)''')

        cursor.execute('Select * From Miners')

        self.miners = cursor.fetchall()

        print(self.miners)

        connection.commit()
        connection.close()

    def add_miner(ip, username, password):
        connection = sqlite3.connect('miners.db')
        cursor = connection.cursor()

        cursor.execute('''INSERT INTO Miners (IP, Username, Password)
                            VALUES({ip},{username}, {password} )''')
        
        connection.commit()
        connection.close()

    def delete_miner(ip):
        connection = sqlite3.connect('miners.db')
        cursor = connection.cursor()

        cursor.execute('''DELETE FROM Miners WHERE IP = {ip} ''')
#
#       Miner Connection Class
#

class minerRequest:
    def __init__(self, username, password, ip):
        self.account = username
        self.password = password
        self.url = "http://" + ip

    def get_miner_status(self):
        
        response = requests.get(self.url + "/cgi-bin/get_miner_status.cgi", auth=HTTPDigestAuth(self.account, self.password))

        return response


db_connect = db()
miners = db_connect.miners

for x in miners:
    print(x)

    miner = minerRequest(x[1], x[2], x[0])
    response = miner.get_miner_status()
    data = response.json()

    freq_arr = data['devs'][0]['freq'].split(',')
    map = {}


    for x in freq_arr:
        temp = x.split('=')
        
        try:
            map[temp[0]] = temp[1]

        except IndexError:
            map[temp[0]] = False


    print("======================================================================================")
    print("              SUMMARY")
    print("GH/S(RT): ", data['summary']['ghs5s'])
    print("GH/S(avg): ", data['summary']['ghsav'])
    print("Fan 1: ", map['fan3'], " | Fan 2: ", map['fan6'])
    print("\n             ANTMINER")
    print("ASIC Board 1")
    print("GH/S(RT): ", map['chain_rate6'])
    print("Temp(Chip1): ", map['temp6'])
    print("Temp(Chip2): ", map['temp2_6'])
    print("ASIC Status: ", map['chain_acs6'])
    print("\nASIC Board 2")
    print("GH/S(RT): ", map['chain_rate7'])
    print("Temp(Chip1): ", map['temp7'])
    print("Temp(Chip2): ", map['temp2_7'])
    print("ASIC Status: ", map['chain_acs7'])
    print("\nASIC Board 3")
    print("GH/S(RT): ",  map['chain_rate8'])
    print("Temp(Chip1): ", map['temp7'])
    print("Temp(Chip2): ", map['temp2_8'])
    print("ASIC Status: ", map['chain_acs8'])
    print("=======================================================================================")