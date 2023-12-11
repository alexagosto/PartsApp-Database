from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

front_stats_handler = Blueprint('front_stats_handler', __name__)


@front_stats_handler.route('/transactions/<int:warehouse_id>', methods=['GET'])
def get_all_transactions(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_front_stats_dao()

    try:
        results = stats.get_all_transactions(warehouse_id)
        response = []
        for result in results:
            response_data = {
                'TransactionID': result[0],
                'UserID': result[1],
                'TransactionDate': result[2],
                'Profit': result[3]
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


@front_stats_handler.route('/supplier_parts/<int:supplier_id>', methods=['GET'])
def get_all_parts_by_supplier(supplier_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_front_stats_dao()

    try:
        results = stats.get_all_parts_by_supplier(supplier_id)
        response = []
        for result in results:
            response_data = {
                'PartID': result[0],
                'PartName': result[1],
                'PartPrice': result[2],
                'PartType': result[3]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message=f'Supplier #{supplier_id} supplies no parts')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500


@front_stats_handler.route('/warehouse_parts/<int:warehouse_id>', methods=['GET'])
def get_all_parts_by_warehouse(warehouse_id):
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_front_stats_dao()

    try:
        results = stats.get_all_parts_by_warehouse(warehouse_id)
        response = []
        for result in results:
            response_data = {
                'PartID': result[0],
                'PartName': result[1],
                'PartPrice': result[2],
                'PartType': result[3]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message=f'Warehouse #{warehouse_id} has no parts')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500


@front_stats_handler.route('/part_prices', methods=['GET'])
def get_all_part_prices():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_front_stats_dao()

    try:
        results = stats.get_all_part_prices()
        response = []
        for result in results:
            response_data = {
                'PartID': result[0],
                'PartName': result[1],
                'PartType': result[2],
                'PartPrice': result[3]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            stats.rollback()
            return jsonify(message=f'There are no part records')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500