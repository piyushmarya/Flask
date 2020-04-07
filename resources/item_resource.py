import sqlite3
import os
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        help = "price of product",
                        required = True
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
                return item.json()
        return {"msg":"item not found"},404

    def post(self, name):
        if ItemModel.get_item_by_name(name):
                return {"msg":"Item with name {} already exixts".format(name)},400
        data = self.parser.parse_args()
        item = ItemModel(name,data['price'])
        item.save_to_db()
        return {"name":name, "price":data['price']}, 201

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item is not None:
            item.delete_from_db()
            return {"msg":"Deleted"},200

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        if item:
            item.price = data['price']
            item.save_to_db()
            return {"msg":"item updated"},200
        else:
            item = ItemModel(name, data['price'])
            item.save_to_db()
            return {"msg":"new item created"},201
        return {"msg":"unknown error"},400


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]},201
