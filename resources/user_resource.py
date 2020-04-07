from flask_restful import Resource, reqparse
from models.user_model import UserModel


class RegistorUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        help="Required Field",
                        required=True)
    parser.add_argument('password',
                        help="Required Field",
                        required=True)

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"msg":"user already exists"},400
        user = UserModel(**data)
        user.save_to_db()
        return {"msg":"created user"},201
