from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars

from src.models.register_model import RegisterModel
from src.models.store_model import StoreModel

blp = Blueprint("Register", __name__, description="Registro do totem na loja")

@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterModel)
    @blp.response(200, StoreModel)
    def post(self, store_data):
        try:   
            store = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one_and_update({"_id": ObjectId(store_data["storeId"])}, {"$push": {"equipments": store_data["tokenId"]}})
            
            if store == None:
                abort(404, message="Store not found")
            
            store["tokens"].append(store_data["tokenId"])
            return store
        
        except KeyError:
            abort(500, message="Error getting the store.")