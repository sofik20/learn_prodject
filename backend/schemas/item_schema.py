from apiflask import Schema
from apiflask.fields import Integer, String, List, Nested


class ItemSchema(Schema):
    id = Integer()
    name = String()


class ItemsOutSchema(Schema):
    items = List(Nested(ItemSchema))