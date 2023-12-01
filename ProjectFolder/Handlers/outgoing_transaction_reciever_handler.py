from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

outgoing_transaction_receiver_handler = Blueprint('outgoing_transaction_reciever_handler', __name__)


@outgoing_transaction_receiver_handler.route('/', methods=['POST'])
def create_receiver():
    data = request.get_json()
    receiver_name = data.get('ReceiverName')

    dao_factory = DAOFactory(conn)
    receiver_dao = dao_factory.get_outgoing_transaction_receivers_dao()

    try:
        receivers = receiver_dao.create_receivers(receiver_name)
        response = {
            'message': 'Receiver created successfully',
            'ReceiverID': receivers[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        receiver_dao.rollback()
        return jsonify(error=error_message), 500


@outgoing_transaction_receiver_handler.route('/', methods=['GET'])
def get_receivers():
    dao_factory = DAOFactory(conn)
    receivers_dao = dao_factory.get_outgoing_transaction_receivers_dao()

    receivers = receivers_dao.get_receivers()

    try:
        response = []
        for receiver in receivers:
            transaction_data = {
                'ReceiverID': receiver[0],
                'ReceiverName': receiver[1],
            }
            response.append(transaction_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        receivers_dao.rollback()
        return jsonify(error=error_message), 500


@outgoing_transaction_receiver_handler.route('/<int:receiver_id>', methods=['GET'])
def get_receivers_by_id(receiver_id):
    dao_factory = DAOFactory(conn)
    receivers_dao = dao_factory.get_outgoing_transaction_receivers_dao()

    try:
        receiver = receivers_dao.get_receivers_by_id(receiver_id)
        if receiver:
            response = {
                'ReceiverID': receiver[0],
                'ReceiverName': receiver[1],
            }

            return jsonify(response)
        else:
            return jsonify(error='Receiver not found'), 404

    except Exception as e:
        error_message = str(e)
        receivers_dao.rollback()
        return jsonify(error=error_message), 500


@outgoing_transaction_receiver_handler.route('/<int:receiver_id>', methods=['PUT'])
def update_transactions(receiver_id):
    data = request.get_json()
    receiver_name = data.get('ReceiverName')


    dao_factory = DAOFactory(conn)
    receivers_dao = dao_factory.get_outgoing_transaction_receivers_dao()

    try:
        receivers_dao.update_receivers_by_id(receiver_id, receiver_name)
        receiver = receivers_dao.get_receivers_by_id(receiver_id)
        if receiver and (
                receiver[1] == receiver_name
        ):
            return jsonify(message=f'Receiver {receiver_id} updated successfully')

        else:
            return jsonify(error='Receiver not found'), 404

    except Exception as e:
        error_message = str(e)
        receivers_dao.rollback()
        return jsonify(error=error_message), 500

