from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify 
 
app = Flask(__name__)
api = Api(app)
 
db_connect = create_engine('sqlite:///chinook.db', connect_args={'check_same_thread': False})
conn = db_connect.connect() 
 
class Employees(Resource):
    def get(self):
        query = conn.execute("select * from employees") 
        return {'employees': [i[0] for i in query.cursor.fetchall()]} 
 
class Tracks(Resource):
    def get(self):
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
 
class Employees_Name(Resource):
    def get(self, employee_id):
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        
 
api.add_resource(Employees, '/employees') 
api.add_resource(Tracks, '/tracks') 
api.add_resource(Employees_Name, '/employees/<employee_id>') 
 
if __name__ == '__main__':
     app.run()