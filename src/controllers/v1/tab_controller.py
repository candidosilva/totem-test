from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from src.functions.tab_functions import creditPaymentMethod, debitPaymentMethod, pixPaymentMethod

from src.models.tab_model import TabModel, ItemModel, TabPayment

blp = Blueprint("Tabs", __name__, description="Acesso as comandas da loja")

@blp.route("/tab")
class InsertTab(MethodView):
    @blp.arguments(TabModel)
    @blp.response(201, TabModel)
    def post(self, tab_data):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one_and_update({"_id": ObjectId(tab_data["storeId"])}, {"$push": {"tabs": {"number": tab_data["tabNumber"], "itens": []}}})
            new_tab = {**tab_data, "id": dbResponse.inserted_id}

            return new_tab
        
        except KeyError:
            abort(500, message="Error creating tab.")
            
@blp.route("/tab")
class UpdateTab(MethodView):
    @blp.arguments(TabModel)
    @blp.response(200, ItemModel)
    def patch(self, tab_data):
        try:
            MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].update_one({"_id": ObjectId(tab_data["storeId"]), "tabs.number": tab_data["tabNumber"]}, {"$push": {"tabs.$.itens": tab_data["item"]}})

            return tab_data.items
        
        except KeyError:
            abort(500, message="Error updating tab.")

@blp.route("/tab/<string:store_id>/<string:tab_number>")
class TabItens(MethodView):
    @blp.response(200, ItemModel(many=True))
    def get(self, store_id, tab_number):
        try:
            store = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one({"_id": ObjectId(store_id)})
            
            if store == None:
                abort(404, message="Store not found")

            tab = find(store["itens"], tab_number)
            
            return tab["itens"]

        except KeyError:
            abort(500, message="Error getting the store.")

@blp.route("/tab/payment")
class TabPayment(MethodView):
    @blp.arguments(TabPayment)
    def post(self, tab):
        try:
            if tab["paymentMethod"] == 1:
                creditPaymentMethod(tab)
            elif tab["paymentMethod"] == 2:
                debitPaymentMethod(tab)
            else:
                pixPaymentMethod(tab)
            

        except KeyError:
            abort(500, message="Payment Error.")
            
def find(arr, elem):
    for x in arr:
       if x == elem:
           return x
    else:
        return None 