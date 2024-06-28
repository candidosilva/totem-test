from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars

from src.models.store_model import StoreModel

blp = Blueprint("Stores", __name__, description="Acesso as stores")

@blp.route("/store")
class Store(MethodView):
    @blp.arguments(StoreModel)
    @blp.response(201, StoreModel)
    def post(self, store_data):
        try:
            new_store = {**store_data}
            print("***********************")
            print(MongoDBConnection)
            print("***********************")
            print("***********************")
            print(globalvars.CONST_STORES_COLLECTION)
            print("***********************")
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].insert_one(new_store)
            store_response = {**store_data, "id": dbResponse.inserted_id, "tokens": [], "tabs": []}
            return store_response
        
        except KeyError:
            abort(500, message="Error creating store.")

@blp.route("/store/<string:store_id>")
class StoreList(MethodView):
    @blp.response(200, StoreModel)
    def get(self, store_id):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one({"_id": ObjectId(store_id)})
            
            if dbResponse == None:
                abort(404, message="Store not found")

            return dbResponse

        except KeyError:
            abort(500, message="Error getting the store.")