from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'andypassword'
api = Api(app)
jwt = JWT(app, authenticate, identity) # /auth endpoint

items = []
connectionstring = "postgresql://postgres:postgres@pythonflask.eastus.cloudapp.azure.com:5432/costs"

class Item(Resource):
    @jwt_required()        # requires authentication if this is added
    def get(self, name):
        # Next finds next item, if list is empty the program will break so we use None at end to prevent this if list is empty.
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
       

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)            
        return item, 201   

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            #type=float,
            required=True,
            help="this field cannot be left empty"
        )
        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class Items(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(Items, '/items')


app.run(port=5000, debug=True)
