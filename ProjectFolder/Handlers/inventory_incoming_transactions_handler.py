from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

inventory_incoming_transaction_handler = Blueprint('inventory_incoming_transaction_handler', __name__)


@inventory_incoming_transaction_handler.route('/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    part_id = data.get('PartID')
    supplier_id = data.get('SupplierID')
    rack_id = data.get('RackID')
    warehouse_id = data.get('WarehouseID')
    user_id = data.get('UserID')
    transaction_date = data.get('TransactionDate')
    transaction_profit = data.get('Profit')

    dao_factory = DAOFactory(conn)
    transaction_dao = dao_factory.get_inventory_incoming_transactions_dao()

    try:
        transaction = transaction_dao.create_transactions(part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, transaction_profit)
        response = {
            'message': 'Transaction created successfully',
            'Incoming TransactionID': transaction[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        transaction_dao.rollback()
        return jsonify(error=error_message), 500


@inventory_incoming_transaction_handler.route('/', methods=['GET'])
def get_transactions():
    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_inventory_incoming_transactions_dao()

    transactions = transactions_dao.get_transactions()

    try:
        response = []
        for transaction in transactions:
            transaction_data = {
                'transaction_id': transaction[0],
                'part_id': transaction[1],
                'supplier_id': transaction[2],
                'rack_id': transaction[3],
                'warehouse_id': transaction[4],
                'user_id': transaction[5],
                'transaction_date': transaction[6],
                'profit': transaction[7]
            }
            response.append(transaction_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500


@inventory_incoming_transaction_handler.route('/<int:transaction_id>', methods=['GET'])
def get_transactions_by_id(transaction_id):
    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_inventory_incoming_transactions_dao()

    try:
        transaction = transactions_dao.get_transactions_by_id(transaction_id)
        if transaction:
            response = {
                'transaction_id': transaction[0],
                'part_id': transaction[1],
                'supplier_id': transaction[2],
                'rack_id': transaction[3],
                'warehouse_id': transaction[4],
                'user_id': transaction[5],
                'transaction_date': transaction[6],
                'profit': transaction[7]
            }
            return jsonify(response)
        else:
            transactions_dao.rollback()
            return jsonify(error='Transaction not found'), 404

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500


@inventory_incoming_transaction_handler.route('/<int:transaction_id>', methods=['PUT'])
def update_transactions(transaction_id):
    data = request.get_json()
    part_id = data.get('PartID')
    supplier_id = data.get('SupplierID')
    rack_id = data.get('RackID')
    warehouse_id = data.get('WarehouseID')
    user_id = data.get('UserID')
    transaction_date = data.get('TransactionDate')
    transaction_profit = data.get('Profit')

    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_inventory_incoming_transactions_dao()

    try:
        transactions_dao.update_transactions_by_id(transaction_id, part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, transaction_profit)
        transaction = transactions_dao.get_transactions_by_id(transaction_id)
        if transaction and (
                transaction[1] == part_id and
                transaction[2] == supplier_id and
                transaction[3] == rack_id and
                transaction[4] == warehouse_id
        ):
            return jsonify(message=f'Transaction {transaction_id} updated successfully')

        else:
            transactions_dao.rollback()
            return jsonify(error='Transaction not found'), 404

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500

