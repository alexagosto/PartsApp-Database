from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn


parts_handler = Blueprint('parts_handler', __name__)


@parts_handler.route('/', methods=['POST'])
def create_part():
    data = request.get_json()
    part_name = data.get('PartName')
    part_type = data.get('PartType')
    part_price = data.get('PartPrice')

    dao_factory = DAOFactory(conn)
    PartsDAO = dao_factory.get_parts_dao()

    try:
        part_id = PartsDAO.create_parts(part_name, part_type, part_price)
        response = {
            'message': 'Part created successfully',
            'PartID': part_id[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        PartsDAO.rollback()
        return jsonify(error=error_message), 500


@parts_handler.route('/', methods=['GET'])
def get_parts():
    dao_factory = DAOFactory(conn)
    PartsDAO = dao_factory.get_parts_dao()

    parts = PartsDAO.get_parts()

    try:
        response = []
        for part in parts:
            part_data = {
                'part_id': part[0],
                'part_name': part[1],
                'part_type': part[2],
                'part_price' : part[3]
            }
            response.append(part_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        PartsDAO.rollback()
        return jsonify(error=error_message), 500


@parts_handler.route('/<int:part_id>', methods=['GET'])
def get_part_by_id(part_id):
    dao_factory = DAOFactory(conn)
    PartsDAO = dao_factory.get_parts_dao()

    try:
        part = PartsDAO.get_part_by_id(part_id)
        if part:
            response = {
                'part_name': part[1],
                'part_type': part[2],
                'part_price': part[3]
            }

            return jsonify(response)
        else:
            PartsDAO.rollback()
            return jsonify(error='Part not found'), 404

    except Exception as e:
        error_message = str(e)
        PartsDAO.rollback()
        return jsonify(error=error_message), 500


@parts_handler.route('/<int:part_id>', methods = ['PUT'])
def update_part(part_id):
    data = request.get_json()
    new_part_name = data.get('PartName')
    new_part_type = data.get('PartType')
    new_part_price = data.get('PartPrice')
    dao_factory = DAOFactory(conn)
    PartsDAO = dao_factory.get_parts_dao()

    try:
        PartsDAO.update_part_by_id(part_id, new_part_name, new_part_type, new_part_price)
        part = PartsDAO.get_part_by_id(part_id)
        if part and (part[1] == new_part_name and part[2] == new_part_type and part[3] == new_part_price):
            return jsonify(message=f'Part {part_id} updated successfully')

        else:
            PartsDAO.rollback()
            return jsonify(error='Part not found'), 404

    except Exception as e:
        error_message = str(e)
        PartsDAO.rollback()
        return jsonify(error=error_message), 500


@parts_handler.route('/<int:part_id>', methods=['DELETE'])
def delete_part(part_id):
    dao_factory = DAOFactory(conn)
    PartsDAO = dao_factory.get_parts_dao()

    try:
        part = PartsDAO.get_part_by_id(part_id)
        if part:
            PartsDAO.delete_part_by_id(part_id)
            if not PartsDAO.get_part_by_id(part_id):
                return jsonify(message=f'Part {part_id} deleted successfully')
            else:
                return jsonify(error='Part could not be deleted'), 404

        else:
            PartsDAO.rollback()
            return jsonify(error='Part not found'), 404

    except Exception as e:
        error_message = str(e)
        PartsDAO.rollback()
        return jsonify(error=error_message), 500