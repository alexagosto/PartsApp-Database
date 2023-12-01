from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

most_global_statistics_handler = Blueprint('most_global_statistics_handler', __name__)


@most_global_statistics_handler.route('/rack', methods=['GET'])
def get_most_rack():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_most_global_statistics_dao()

    try:
        results = stats.get_most_rack()
        response = []
        for result in results:
            response_data = {
                'WarehouseID': result[0],
                'WarehouseName': result[1],
                'Count of Racks per Warehouse': result[2]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            return jsonify(message='Warehouse rack count could not be found')

    except Exception as e:
        error_message = str(e)
        return jsonify(error=error_message), 500


@most_global_statistics_handler.route('/incoming', methods=['GET'])
def get_most_incoming():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_most_global_statistics_dao()

    try:
        results = stats.get_most_incoming()
        response = []
        for result in results:
            response_data = {
                'WarehouseID': result[0],
                'WarehouseName': result[1],
                'Count of Incoming Transactions per Warehouse': result[2]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message='Warehouse transaction count could not be found')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500


@most_global_statistics_handler.route('/deliver', methods=['GET'])
def get_most_deliver():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_most_global_statistics_dao()

    try:
        results = stats.get_most_deliver()
        response = []
        for result in results:
            response_data = {
                'WarehouseID': result[0],
                'WarehouseName': result[1],
                'Count of Delivered Exchanges per Warehouse': result[2]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message='Warehouse exchange count could not be found')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500


@most_global_statistics_handler.route('/transactions', methods=['GET'])
def get_most_transactions():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_most_global_statistics_dao()

    try:
        results = stats.get_most_transactions()
        response = []
        for result in results:
            response_data = {
                'UserId': result[0],
                'Username': result[1],
                'Count of Transactions per User': result[2]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message='User transaction count could not be found')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500


@most_global_statistics_handler.route('/city', methods=['GET'])
def get_most_city():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_most_global_statistics_dao()

    try:
        results = stats.get_most_city()
        response = []
        for result in results:
            response_data = {
                'WarehouseCity': result[0],
                'Count of Transactions per City': result[1]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message='City transaction count could not be found')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500