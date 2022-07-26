from flask import jsonify
import requests
import json

url = 'http://192.168.0.10:8090/nlc02api'


door_status = {'cmd': 'doorstat', 'bus': 0}
module_status = {'cmd': 'modstat', 'bus': 0}

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


    

















