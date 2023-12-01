from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

user_handler = Blueprint('user_handler', __name__)


@user_handler.route('/', methods=['POST'])
def create_users():
    data = request.get_json()
    username = data.get('Username')
    warehouse_id = data.get('WarehouseID')
    email = data.get('UserEmail')

    dao_factory = DAOFactory(conn)
    user_dao = dao_factory.get_users_dao()

    try:
        user_id = user_dao.create_user(username, warehouse_id, email)
        response = {
            'message': 'User created successfully',
            'UserID': user_id[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        user_dao.rollback()
        return jsonify(error=error_message), 500


@user_handler.route('/', methods=['GET'])
def get_users():
    dao_factory = DAOFactory(conn)
    user_dao = dao_factory.get_users_dao()

    users = user_dao.get_users()

    try:
        response = []
        for user in users:
            user_data = {
                'user_id': user[0],
                'username': user[1],
                'warehouse_id': user[2],
                'user_email': user[3]
            }
            response.append(user_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        user_dao.rollback()
        return jsonify(error=error_message), 500


@user_handler.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    dao_factory = DAOFactory(conn)
    user_dao = dao_factory.get_users_dao()

    try:
        user = user_dao.get_user_by_id(user_id)
        if user:
            response = {
                'username': user[1],
                'warehouse_id': user[2],
                'user_email': user[3]
            }

            return jsonify(response)
        else:
            user_dao.rollback()
            return jsonify(error='User not found'), 404

    except Exception as e:
        error_message = str(e)
        user_dao.rollback()
        return jsonify(error=error_message), 500


@user_handler.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    new_username = data.get('UserName')
    new_warehouse = data.get('WarehouseID')
    email = data.get('UserEmail')
    dao_factory = DAOFactory(conn)
    user_dao = dao_factory.get_users_dao()

    try:
        user_dao.update_user_by_id(user_id, new_username, new_warehouse, email)
        user = user_dao.get_user_by_id(user_id)
        if user and (
                user[1] == new_username and
                user[2] == new_warehouse and
                user[3] == email
        ):
            return jsonify(message=f'User {user_id} updated successfully')

        else:
            user_dao.rollback()
            return jsonify(error='User not found'), 404

    except Exception as e:
        error_message = str(e)
        user_dao.rollback()
        return jsonify(error=error_message), 500


@user_handler.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    dao_factory = DAOFactory(conn)
    user_dao = dao_factory.get_users_dao()

    try:
        user = user_dao.get_user_by_id(user_id)
        if user:
            user_dao.delete_user_by_id(user_id)
            if not user_dao.get_user_by_id(user_id):
                return jsonify(message=f'User {user_id} deleted successfully')
            else:
                return jsonify(error='User not found'), 404
        else:
            user_dao.rollback()
            return jsonify(error='User not found'), 404

    except Exception as e:
        error_message = str(e)
        user_dao.rollback()
        return jsonify(error=error_message), 500