from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

local_statistics_handler = Blueprint('local_statistics_handler', __name__)


@local_statistics_handler.route('/<int:warehouse_id>/profit', methods=['POST'])
def get_warehouse_profits(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            results = stats.get_warehouse_profit(warehouse_id)
            response = []
            for result in results:
                response_data = {
                    'WarehouseID': result[0],
                    'Profit': result[1],
                    'Year': result[2]
                }
                response.append(response_data)

            if response:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'Warehouse #{warehouse_id} has no records')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/rack/lowstock', methods=['POST'])
def get_rack_lowstock(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            low_stock = stats.get_rack_lowstock(warehouse_id)
            response = []
            for stock in low_stock:
                response_data = {
                    'RackID': stock[0],
                    'Rack Capacity': str(stock[1]*100)+'%'
                }
                response.append(response_data)

            if response:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No such racks found at Warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/rack/material', methods=['POST'])
def get_rack_material(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            materials = stats.get_rack_material(warehouse_id)
            response = []
            for material in materials:
                response_data = {
                    'Part Material 1=Metal, 2=Rubber, 3=Polymer, 4=Fluid': material[1],
                    'Part Count in Warehouse': material[0]
                }
                response.append(response_data)

            if response:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No parts found at warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/rack/expensive', methods=['POST'])
def get_rack_expensive(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            expensive = stats.get_rack_expensive(warehouse_id)
            response = []
            for expense in expensive:
                response_data = {
                    'RackID': expense[0],
                    'Rack Total Value': expense[1]
                }
                response.append(response_data)
            if expensive:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No racks at warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/transaction/suppliers', methods=['POST'])
def get_transaction_suppliers(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            suppliers = stats.get_transaction_suppliers(warehouse_id)
            response = []
            for supplier in suppliers:
                response_data = {
                    'SupplierID': supplier[0],
                    f'Count of Supplies Supplied to Warehouse #{warehouse_id}': supplier[1]
                }
                response.append(response_data)
            if suppliers:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No suppliers have supplied warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/transaction/leastcost', methods=['POST'])
def get_transaction_leastcost(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            costs = stats.get_transaction_leastcost(warehouse_id)
            response = []
            for cost in costs:
                response_data = {
                    'TransactionDate': cost[0],
                    'Profit': cost[1]
                }
                response.append(response_data)

            if response:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No incoming transactions have been made by Warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')


@local_statistics_handler.route('/<int:warehouse_id>/users/receivesmost', methods=['POST'])
def get_users_receivesmost(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_local_statistics_dao()
    data = request.get_json()
    login = data.get('UserID')

    if login == 2:
        try:
            users = stats.get_users_receivesmost(warehouse_id)
            response = []
            for user in users:
                response_data = {
                    'UserID': user[0],
                    'Username': user[1],
                    'Transaction_Count': user[2]
                }
                response.append(response_data)

            if response:
                return jsonify(response), 201
            else:
                stats.rollback()
                return jsonify(message=f'No exchange transactions have been made by users in Warehouse #{warehouse_id}')

        except Exception as e:
            error_message = str(e)
            stats.rollback()
            return jsonify(error=error_message), 500

    else:
        return jsonify(message='User Access not allowed.')

