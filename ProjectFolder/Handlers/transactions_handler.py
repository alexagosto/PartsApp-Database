from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

transaction_handler = Blueprint('transaction_handler', __name__)


@transaction_handler.route('/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    user_id = data.get('UserID')
    transaction_date = data.get('TransactionDate')
    transaction_profit = data.get('Profit')

    dao_factory = DAOFactory(conn)
    transaction_dao = dao_factory.get_transactions_dao()

    try:
        transaction = transaction_dao.create_transactions(user_id, transaction_date, transaction_profit)
        response = {
            'message': 'Transaction created successfully',
            'TransactionID': transaction[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        transaction_dao.rollback()
        return jsonify(error='Error creating transaction, verify date matches format: (YYYY-MM-DD'), 500


@transaction_handler.route('/', methods=['GET'])
def get_transactions():
    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_transactions_dao()

    transactions = transactions_dao.get_transactions()

    try:
        response = []
        for transaction in transactions:
            transaction_data = {
                'transaction_id': transaction[0],
                'user_id': transaction[1],
                'transaction_date': transaction[2],
                'transaction_profit': transaction[3]
            }
            response.append(transaction_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500


@transaction_handler.route('/<int:transaction_id>', methods=['GET'])
def get_transactions_by_id(transaction_id):
    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_transactions_dao()

    try:
        transactions = transactions_dao.get_transactions_by_id(transaction_id)
        if transactions:
            response = {
                'transaction_id': transactions[0],
                'user_id': transactions[1],
                'transaction_date': transactions[2],
                'transaction_profit': transactions[3]
            }

            return jsonify(response)
        else:
            return jsonify(error='Transaction not found'), 404

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500


@transaction_handler.route('/<int:transaction_id>', methods=['PUT'])
def update_transactions(transaction_id):
    data = request.get_json()
    user_id = data.get('UserID')
    transaction_date = data.get('TransactionDate')
    transaction_profit = data.get('Profit')
    dao_factory = DAOFactory(conn)
    transactions_dao = dao_factory.get_transactions_dao()

    try:
        transactions_dao.update_transactions_by_id(transaction_id, user_id, transaction_date, transaction_profit)
        transaction = transactions_dao.get_transactions_by_id(transaction_id)
        if transaction and (
                transaction[1] == user_id and
                transaction[2] == transaction_date and
                transaction[3] == transaction_profit
        ):
            return jsonify(message=f'Transaction {transaction_id} updated successfully')

        else:
            transactions_dao.rollback()
            return jsonify(error='Transaction not found'), 404

    except Exception as e:
        error_message = str(e)
        transactions_dao.rollback()
        return jsonify(error=error_message), 500

