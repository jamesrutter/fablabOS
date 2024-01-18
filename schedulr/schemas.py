from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)


class EquipmentSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class ReservationSchema(Schema):
    user_id = fields.Int(required=True)
    equipment_id = fields.Int(required=True)
    time_slot_id = fields.Int(required=True)
