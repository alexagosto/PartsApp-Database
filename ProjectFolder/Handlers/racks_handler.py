from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

racks_handler = Blueprint('racks_handler', __name__)

@racks_handler.route('/', methods=['POST'])
def create_rack():
    data = request.get_json()
    rack_capacity = data.get('RackCapacity')
    rack_quantity = data.get('RackQuantity')
    rack_warehouse_id = data.get('WarehouseID')

    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()

    try:
        rack_id = RacksDAO.create_rack(rack_capacity, rack_quantity, rack_warehouse_id)
        response = {
            'message': 'Rack created successfully',
            'RackID': rack_id[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500


@racks_handler.route('/', methods=['GET'])
def get_rack():
    
    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()

    racks = RacksDAO.get_racks()

    try:
        response = []
        for rack in racks:
            rack_data = {
                'rack_id': rack[0],
                'rack_capacity': rack[1],
                'rack_quantity': rack[2],
                'rack_warehouse_id' : rack[3]
            }
            response.append(rack_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500


@racks_handler.route('/<int:rack_id>', methods=['GET'])
def get_rack_by_id(rack_id):
    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()
    
    try:
        rack = RacksDAO.get_rack_by_id(rack_id)
        if rack:
            response = {
                'rack_capacity': rack[1],
                'rack_quantity': rack[2],
                'rack_warehouse_id' : rack[3]
            }

            return jsonify(response)
        else:
            RacksDAO.rollback()
            return jsonify(error='Rack not found'), 404

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500

#confirm route and method

@racks_handler.route('/rack/<int:warehouse_id>', methods=['GET'])
def get_rack_by_warehouse_id(warehouse_id):
    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()

    try:
        racks = RacksDAO.get_racks_by_warehouse_id(warehouse_id)
        response = []
        for rack in racks:
            rack_data = {
                'rack_id': rack[0],
                'rack_capacity': rack[1],
                'rack_quantity': rack[2],
                'rack_warehouse_id' : rack[3]
            }
            response.append(rack_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500


@racks_handler.route('/<int:rack_id>', methods = ['PUT'])
def update_rack(rack_id):
    data = request.get_json()
    new_rack_capacity = data.get('RackCapacity')
    new_rack_quantity = data.get('RackQuantity')
    new_rack_warehouse_id = data.get('WarehouseID')
    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()

    try:
        RacksDAO.update_rack_by_id(rack_id, new_rack_capacity, new_rack_quantity, new_rack_warehouse_id)
        rack = RacksDAO.get_rack_by_id(rack_id)
        if rack and (rack[1] == new_rack_capacity and rack[2] == new_rack_quantity and rack[3] == new_rack_warehouse_id):
            return jsonify(message=f'Rack {rack_id} updated successfully')

        else:
            RacksDAO.rollback()
            return jsonify(error='Rack not found'), 404

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500



@racks_handler.route('/<int:rack_id>', methods=['DELETE'])
def delete_rack(rack_id):
    dao_factory = DAOFactory(conn)
    RacksDAO = dao_factory.get_racks_dao()

    try:
        rack = RacksDAO.get_rack_by_id(rack_id)
        if rack:
            RacksDAO.delete_rack_by_id(rack_id)
            if not RacksDAO.get_rack_by_id(rack_id):#If it doesnt exist, we deleted it
                return jsonify(message=f'Rack {rack_id} deleted successfully')
            else:
                return jsonify(error='Rack could not be deleted'), 404

        else:
            RacksDAO.rollback()
            return jsonify(error='Rack not found'), 404

    except Exception as e:
        error_message = str(e)
        RacksDAO.rollback()
        return jsonify(error=error_message), 500