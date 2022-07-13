from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import logging
import nlc
import response
import reboot
import monitor

logger = logging.getLogger()

@app.route('/sibox', methods=['POST'])

def service():

    r = {
            "code" : "0",
            "latency" : "time",
            "message" : "Success",
            "param" : "None"
        }
    
    d = dict()

    try :

        start = response.start_time()
        payload = request.json
        command = payload['cmd']
        param = payload['param']
        r["param"] = param

        if command == 'open':

            if param >= 1:
                nlc.door(param)
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                r["param"] = param
                return jsonify(r)

            else:
                end = response.end_time()
                r["code"] = "101"
                r["message"] = "Parameter is not valid."
                r["latency"] = response.latency(start,end)
                return jsonify(r)

        elif command == 'doorstat':
            if param >= 1:
                d = nlc.doorStatus(param)
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                response = {
                    "response" : r,
                    "data": d
                }
                return jsonify(response)
            
            else:
                r["code"] = "102"
                r["message"] = "Parameter is not valid."
                r["latency"] = response.latency(start,end)
                return jsonify(r)
                

        elif command == 'machinestat':
            d = monitor.check_monitor()
            end = response.end_time()
            r["latency"] = response.latency(start,end)
            r["param"] = param
            resp = {
                "response" : r,
                "data": d
                }
            return jsonify(resp)
        
        elif command == 'reboot':
            reboot.restart()
            end = response.end_time()
            r["latency"] = response.latency(start,end)
            r["param"] = param
            return jsonify(r)
        
        return jsonify(r)  
          
    except :
        r["code"] = "400"
        r["message"] = "Missing Object."
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)
        
if __name__ == '__main__':
    app.run(debug=True)