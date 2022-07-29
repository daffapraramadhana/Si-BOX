from flask import jsonify
import requests
import json
import time

url = 'http://192.168.0.10:8090/nlc02api'


def door(parameter):
    if parameter is None:
        pass
    else:
        door_open = {'cmd': 'open', 'door': None }
        door_open['door'] = parameter
        #print (door_open)
        r = requests.post(url, json = door_open)
        
    

def doorStatus(parameter):
    if parameter is None:
        pass
    else:
        door_status = {'cmd': 'doorstat', 'bus': 0}
        r = requests.post(url, json = door_status)

        if r.ok:
            r.text
            stat = json.loads(r.text)
            parameter = parameter - 1
            doorstatus = stat["door"][parameter]
            return jsonify(doorstatus)
            

def modStatus(parameter):
    if parameter is None:
        pass
    else:
        mod_stat = {'cmd': 'modstat', 'bus': 0}
        r = requests.post(url, json = mod_stat)

        if r.ok:
            r.text
            stat = json.loads(r.text)
            return jsonify(stat)

def countDoors(parameter):
    if parameter is None:
        pass
    else:
        door_stat1 = {'cmd': 'doorstat', 'bus': 0}
        door_stat2 = {'cmd': 'doorstat', 'bus': 1}
        r1 = requests.post(url, json = door_stat1)
        r2 = requests.post(url, json = door_stat2)
        #print(r1.text)
        #print(r2.text)
        stat1 = json.loads(r1.text)
        stat2 = json.loads(r2.text)
        doors1 = stat1['door']
        doors2 = stat2['door']
        sum_doors = (len (doors1) + len (doors2) + 2)
        print (sum_doors)
        
        return (sum_doors)
    
def openAll(parameter):
    if parameter is None:
        pass
    else:
        count_doors = countDoors(1)

        for i in range (count_doors):
            i += 1
            door_open = {'cmd': 'open', 'door': None }
            door_open['door'] = i
            print (door_open)
            r = requests.post(url, json=door_open)
            time.sleep(1)




    

















