from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from model import Door, db
from escpos.printer import Network
from os.path import exists as file_exists
import logging


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///door.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


import nlc
import response
import monitor
import get_printer 
logger = logging.getLogger()


r = {
    "code" : "0",
    "latency" : "time",
    "message" : "Success",
    "param" : "None"
}
d = dict()

db.init_app(app)

@app.before_first_request

def create_data():
    path = "C:/Si-BOX/_API/door.db"
    # path = 'door.db'
    if file_exists(path):
        pass
        # print("Database Exist")
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
                return jsonify(r)

            else:
                end = response.end_time()
                r["code"] = "102"
                r["message"] = "Parameter is not valid."
                r["latency"] = response.latency(start,end)
                return jsonify(r)

        elif command == 'getallstat':
            if param == 'doors':
                doors = Door.query.all()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                resp = {
                    "response" : r,
                    "data": ([door.to_json() for door in doors])
                }
                return jsonify(resp)

        elif command == 'machinestat':
            if param is not None:
                d = monitor.check_monitor()
                end = response.end_time()
                r["latency"] = response.latency(start,end)
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
                return jsonify(r)
            
    except :
        r["code"] = "400"
        r["message"] = logger()
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)

@app.route('/sibox/ops/edit', methods=['POST'])

def edit():

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

@app.route('/sibox/printer', methods=['POST'])

def printer():
    try: 

        payload = request.json
        start = response.start_time()
        command = payload['cmd']
        param = payload['param']
        data = payload['data']

        if command == 'print':
            try:
                get_printer.check(data)
                IP = data['ip']
                p = Network(f"{IP}")
                if p:
                    try:
                        get_printer.printer(data)
                        end = response.end_time()
                        r["latency"] = response.latency(start,end)
                        r["param"] = param
                        return jsonify(r)

                    except:
                        r["code"] = "402"
                        r["message"] = "IP not valid."
                        end = response.end_time()
                        r["latency"] = response.latency(start,end)
                        return jsonify(r)
            
            except:
                r["code"] = "401"
                r["message"] = "Data not valid."
                end = response.end_time()
                r["latency"] = response.latency(start,end)
                return jsonify(r)

    except:
        r["code"] = "400"
        r["message"] = "Missing Object."
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)            


@app.route('/sibox', methods=['POST'])

def service():
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
            
    except :
        r["code"] = "400"
        r["message"] = "Missing Object."
        end = response.end_time()
        r["latency"] = response.latency(start,end)
        return jsonify(r)
              
if __name__ == '__main__':
    app.run(debug=True)
    # app.debug = True
    # app.run(host="192.168.7.196", port = 5000)