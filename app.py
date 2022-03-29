import requests
from requests.auth import HTTPDigestAuth

class minerRequest:
    def __init__(self, password, url):
        self.account = "root"
        self.password = password
        self.digest_realm = "antMiner Configuration"
        self.qop = "auth"
        self.nonce_count = "0000004e"
        self.url = "http://" + url

    def get_miner_status(self):
        
        response = requests.get(self.url + "/cgi-bin/get_miner_status.cgi", auth=HTTPDigestAuth(self.account, self.password))

        return response


miner1 = minerRequest("tane", "192.168.1.205")
response = miner1.get_miner_status()
data = response.json()

freq_arr = data['devs'][0]['freq'].split(',')
map = {}

freq_arr2 = data['devs'][1]['freq'].split(',')
map2 = {}

for x in freq_arr:
    temp = x.split('=')
    
    try:
        map[temp[0]] = temp[1]
    except IndexError:
        map[temp[0]] = False


for x in freq_arr2:
    temp = x.split('=')
    
    try:
        map2[temp[0]] = temp[1]
    except IndexError:
        map2[temp[0]] = False
# print(map)

print("=====================================")
print("              SUMMARY")
print("GH/S(RT): ", data['summary']['ghs5s'])
print("GH/S(avg): ", data['summary']['ghsav'])
print("\n             ANTMINER")
print("ASIC Board 1")
print("GH/S(RT): ", map['chain_rate6'])
print("Temp(Chip1: ", )
print("Temp(Chip2): ", map['temp2_6'])
print("ASIC Status: ", data['devs'][0]['chain_acs'])
print("\nASIC Board 2")
print("GH/S(RT): ", map2['chain_rate6'])
print("Temp(Chip1: ", )
print("Temp(Chip2): ", freq_arr[16])
print("\nsASIC Board 3")
print("GH/S(RT): ", )
print("Temp(Chip1: ", )
print("Temp(Chip2): ", freq_arr[16])
print("======================================")