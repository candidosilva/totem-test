from marshmallow import Schema,  fields

class ItemModel(Schema):
    name=fields.Str()
    quantity=fields.Int()
    price=fields.Float()

class TabModel(Schema):
    storeId=fields.Str(dump_only=True)
    tabNumber=fields.Int(required=True)
    items=fields.Nested(ItemModel(many=True))

class TabPayment(Schema):
    storeId=fields.Str(dump_only=True)
    cpfOrCnpj=fields.Str()
    email=fields.Str()
    paymentMethod=fields.Str()
    tabs=fields.List(fields.Str(), many=True)