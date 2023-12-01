from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

least_global_statistics_handler = Blueprint('least_global_statistics_handler', __name__)


@least_global_statistics_handler.route('/outgoing', methods=['GET'])
def get_least_outgoing():
    dao_factory = DAOFactory(conn)
    stats = dao_factory.get_least_global_statistics_dao()

    try:
        results = stats.get_least_outgoing()
        response = []
        for result in results:
            response_data = {
                'WarehouseID': result[0],
                'WarehouseName': result[1],
                'Amount of Outgoing Transactions': result[2]
            }
            response.append(response_data)

        if response:
            return jsonify(response), 201
        else:
            return jsonify(message='Warehouse Outgoing records not found.')

    except Exception as e:
        error_message = str(e)
        stats.rollback()
        return jsonify(error=error_message), 500