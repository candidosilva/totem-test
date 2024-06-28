from marshmallow import Schema, fields

class RegisterModel(Schema):
    storeId=fields.Str()
    equipmentId=fields.Str()