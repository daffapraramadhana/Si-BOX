from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from sqlalchemy import DateTime
from model import Door, db
from os.path import exists as file_exists
from datetime import datetime

app = Flask(__name__)
CORS(app)

import nlc
import response
import monitor
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///door.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['']
db.init_app(app)

@app.before_first_request

def create_data():
    if file_exists('door.db'):
        print("Database Exist")
    
    else:
        db.create_all()
        #count_doors = nlc.countDoors(1)
        #print("db created")
        #for i in range (count_doors):
        for i in range (32):
            i += 1
            no = i
            state = 'ENABLE'
            door = Door(no=no, state=state)
            db.session.add(door)
            db.session.commit()
        
            



@app.route('/sibox/ops', methods=['POST'])

def operations():
    r = {
            "code" : "0",
            "latency" : "time",
            "message" : "Success",
            "param" : "None"
        }
    
    d = dict()

    try :

        
        payload = request.json
        command = payload['cmd']
        param = payload['param']
        start = response.start_time()
        # no = payload['no']
        # state = payload['state']
        # status = payload['status']
        r["param"] = param

        if command == 'openall':

            if param >= 1:
                nlc.openAll(param)
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                r["param"] = param
                return jsonify(r)

            else:
                end = response.end_time()
                r["code"] = "102"
                r["message"] = "Parameter is not valid."
                r["latency"] = response.latency(start,end)
                return jsonify(r)

        elif command == 'getallstat':
            if param >= 1:
                doors = Door.query.all()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": ([door.to_json() for door in doors])
                }
                return jsonify(resp)
        
        elif command == 'reboot':
            if param is not None:
                monitor.restart()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                r["param"] = param
                return jsonify(r)
            
    except :
        r["code"] = "400"
        r["message"] = "Missing Object."
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)

@app.route('/sibox/ops/edit', methods=['POST'])
def edit():
    r = {
            "code" : "0",
            "latency" : "time",
            "message" : "Success",
            "param" : "None"
        }
    
    d = dict()

    try :

        payload = request.json
        command = payload['cmd']
        param = payload['param']
        start = response.start_time()
        no = payload['no']
        state = payload['state']
        r["param"] = param
        

        if command == 'delete':
            if param is not None :
                door = Door.query.get(no)
                if door is None:
                    end = response.end_time()
                    r["latency"] = response.latency(start,end)
                    r["message"] = "Door not exist."
                    return jsonify(r)

                db.session.delete(door)
                db.session.commit()
                doors = Door.query.all()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": ([door.to_json() for door in doors])
                    }
                return jsonify(resp)

        elif command == 'add':
            if param is not None:
                exists = db.session.query(db.session.query(Door).filter_by(no=no).exists()).scalar()
                if exists :
                    end = response.end_time()
                    r["latency"] = response.latency(start,end)
                    r["message"] = "Door exists"
                    return jsonify(r)
                
                else:
                    book = Door(no = no, state=state)
                    db.session.add(book)
                    db.session.commit()
                    doors = Door.query.all()
                    end = response.end_time()
                    r["latency"] = response.latency(start,end)
                    resp = {
                        "response" : r,
                        "data": ([door.to_json() for door in doors])
                        }
                    return jsonify(resp)

        elif command == 'update':
            if param is not None:
                door = Door.query.get(no)
                door.state = state
                db.session.commit()
                doors = Door.query.all()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": ([door.to_json() for door in doors])
                    }
                return jsonify(resp)
        

    except :
        r["code"] = "400"
        r["message"] = "Missing Object."
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)

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
            if param == 'all':
                doors = Door.query.all()
                d = ([door.to_json() for door in doors])
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": d
                }

                # print(x['data']['created'])
                return jsonify(resp)
            
            elif param >= 1:
                doors = Door.query.get(param)
                data = doors.to_json()
                no = data['no']
                state = data['state']
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": {
                        "no" : no,
                        "state" : state,
                    }
                }
                return jsonify(resp)

            # if param >= 1:
            #     d = nlc.doorStatus(param)
            #     end = response.end_time()
            #     r["latency"] = response.latency(start,end)
            #     resp = {
            #         "response" : r,
            #         "data": d
            #     }
            #     return jsonify(resp)
            

        elif command == 'machinestat':
            if param is not None:
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
            if param is not None:
                monitor.restart()
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