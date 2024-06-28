from marshmallow import Schema,  fields

class ItensModel(Schema):
    name=fields.Str()
    quantity=fields.Int()
    price=fields.Float()
    
class TabsModel(Schema): 
    number=fields.Int(required=True)
    itens=fields.Nested(ItensModel(many=True))
    
class StoreModel(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    logoUrl=fields.Str(required=True)
    tokens=fields.List(fields.Str(), many=True, required=False)
    tabs=fields.Nested(TabsModel(many=True))