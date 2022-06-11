import requests
from requests.auth import HTTPDigestAuth
import sqlite3
from getpass import getpass
# import tkinter

#####################################################################
#                   Database Connection Class
#####################################################################

class db:
    
    #Constructor calls the database to extract the miners table

    def __init__(self):
        try:
            connection = sqlite3.connect('miners.db')
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS Miners
                            (IP TEXT, Username TEXT, Password TEXT)''')

            cursor.execute('Select * From Miners')

            self.miners = cursor.fetchall()

            print(self.miners)

            connection.commit()
            connection.close()

            print("Connected To DB")
        except Exception as e:
            print("Error Connecting to DB")
            print(e)

    def add_miner(self, ip, username, password):
        try:

            connection = sqlite3.connect('miners.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Miners (IP, Username, Password) VALUES ( ?, ? , ?)', (ip, username, password))
            
            connection.commit() 
            connection.close()

            print("Added Miner Succesfully")
        except Exception as e:
            print("Error Adding Miner to DB")
            print(e)

    def delete_miner(self, ip):
        try:

            connection = sqlite3.connect('miners.db')
            cursor = connection.cursor()

            cursor.execute('DELETE FROM Miners WHERE IP = ?', (ip,))

            connection.commit() 
            connection.close()

            print("Deleted Miner Successfully")
        except Exception as e:
            print("Error Deleting Miner in DB")
            print(e)

############################################################
#               Miner Connection Class
############################################################

class minerRequest:
    def __init__(self, username, password, ip):
        self.account = username
        self.password = password
        self.url = "http://" + ip

    def get_miner_status(self):
        
        response = requests.get(self.url + "/cgi-bin/get_miner_status.cgi", auth=HTTPDigestAuth(self.account, self.password))

        return response


if __name__ == "__main__":

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
        print("======================================================================================")

    print("Press 1 to add a new miner: ")
    print("Press 2 to delete: ")
    choice = int(input())

    if(choice == 1):
        print("Enter IP: ")
        ip = input()
        print("Enter username: ")
        username = input()
        print("Enter password")
        password = input()

        db_connect.add_miner(ip, username, password)

    elif(choice == 2):
        print("Enter ip to delete: ")
        ip = input()
        db_connect.delete_miner(ip)

else:
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

    # print(map)