from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
app.config = SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:5000/doors'
db = SQLAlchemy(app)

class Doors(db.Model):
   __tablename__ = "doors"
   no = db.Column(db.Integer, primary_key=True)
   state = db.Column(db.String(20))
   status = db.Column(db.String(20))

   def create(self):
       db.session.add(self)
       db.session.commit()
       return self

   def __init__(self, state, status):
       self.state = state
       self.status = status

   def __repr__(self):
       return f"{self.no}"

db.create_all()

class DoorSchema(SQLAlchemyAutoSchema):
   class Meta(SQLAlchemyAutoSchema.Meta):
       model = Doors
       sqla_session = db.session
#    no = fields.Number(dump_only=True)
#    state = fields.String(required=True)
#    status = fields.String(required=True)


@app.route('/api/doors', methods=['POST'])
def create_doors():
   data = request.get_json()
   door_schema = DoorSchema()
   door = door_schema.load(data)
   result = door_schema.dump(door.create())
   return make_response(jsonify({"door": result}), 200)

@app.route('/api/doors', methods=['GET'])
def index():
   get_doors = Doors.query.all()
   door_schema = DoorSchema(many=True)
   todos = door_schema.dump(get_doors)
   return make_response(jsonify({"todos": todos}))

@app.route('/api/doors/<no>', methods=['PUT'])
def update_todo_by_id(id):
   data = request.get_json()
   get_door = Doors.query.get(id)
   if data.get('state'):
       get_door.state = data['state']
   db.session.add(get_door)
   db.session.commit()
   door_schema = DoorSchema(only=['id', 'state'])
   door = door_schema.dump(get_door)

   return make_response(jsonify({"door": door}))