from flask import Flask
from flask_restful import Resource, Api
import model

app = Flask(__name__)
api = Api(app)

class Pong(Resource):
    def get(self):
        return {'message': 'pong'}
class TemperatureController(Resource):
    def get(self):
        return model.get_temperature()

api.add_resource(Pong, '/')
api.add_resource(TemperatureController, '/temperature')
if __name__ == '__main__':
    model.initialize_db()
    app.run()

