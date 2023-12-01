from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

warehouse_handler = Blueprint('warehouse_handler', __name__)


@warehouse_handler.route('/', methods=['POST'])
def create_warehouses():
    data = request.get_json()
    warehouse_name = data.get('WarehouseName')
    warehouse_address = data.get('WarehouseAddress')
    warehouse_city = data.get('WarehouseCity')
    warehouse_budget = data.get('WarehouseBudget')

    dao_factory = DAOFactory(conn)
    warehouse_dao = dao_factory.get_warehouses_dao()

    try:
        warehouse_id = warehouse_dao.create_warehouse(warehouse_name, warehouse_address, warehouse_city, warehouse_budget)
        response = {
            'message': 'Warehouse created successfully',
            'WarehouseID': warehouse_id[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        warehouse_dao.rollback()
        return jsonify(error=error_message), 500


@warehouse_handler.route('/', methods=['GET'])
def get_warehouses():
    dao_factory = DAOFactory(conn)
    warehouse_dao = dao_factory.get_warehouses_dao()

    warehouses = warehouse_dao.get_warehouses()

    try:
        response = []
        for warehouse in warehouses:
            warehouse_data = {
                'WarehouseID': warehouse[0],
                'WarehouseName': warehouse[1],
                'WarehouseAddress': warehouse[2],
                'WarehouseCity': warehouse[3],
                'Budget': warehouse[4]
            }
            response.append(warehouse_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        warehouse_dao.rollback()
        return jsonify(error=error_message), 500


@warehouse_handler.route('/<int:warehouse_id>', methods=['GET'])
def get_warehouse_by_id(warehouse_id):
    dao_factory = DAOFactory(conn)
    warehouse_dao = dao_factory.get_warehouses_dao()

    try:
        warehouse = warehouse_dao.get_warehouse_by_id(warehouse_id)
        if warehouse:
            response = {
                'WarehouseID': warehouse[0],
                'WarehouseName': warehouse[1],
                'WarehouseAddress': warehouse[2],
                'WarehouseCity': warehouse[3],
                'Budget': warehouse[4]
            }

            return jsonify(response)
        else:
            warehouse_dao.rollback()
            return jsonify(error='Warehouse not found'), 404

    except Exception as e:
        error_message = str(e)
        warehouse_dao.rollback()
        return jsonify(error=error_message), 500


@warehouse_handler.route('/<int:warehouse_id>', methods=['PUT'])
def update_warehouse(warehouse_id):
    data = request.get_json()
    new_warehouse_name = data.get('WarehouseName')
    new_warehouse_address = data.get('WarehouseAddress')
    new_warehouse_city = data.get('WarehouseCity')
    new_warehouse_budget = data.get('Budget')
    dao_factory = DAOFactory(conn)
    warehouse_dao = dao_factory.get_warehouses_dao()

    try:
        warehouse_dao.update_warehouse_by_id(warehouse_id, new_warehouse_name, new_warehouse_address, new_warehouse_city, new_warehouse_budget)
        warehouse = warehouse_dao.get_warehouse_by_id(warehouse_id)
        if warehouse and (
                warehouse[1] == new_warehouse_name and
                warehouse[2] == new_warehouse_address and
                warehouse[3] == new_warehouse_city and
                warehouse[4] == new_warehouse_budget
        ):
            return jsonify(message=f'Warehouse {warehouse_id} updated successfully')

        else:
            return jsonify(error='Warehouse not found'), 404

    except Exception as e:
        error_message = str(e)
        warehouse_dao.rollback()
        return jsonify(error=error_message), 500


@warehouse_handler.route('/<int:warehouse_id>', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    dao_factory = DAOFactory(conn)
    warehouse_dao = dao_factory.get_warehouses_dao()

    try:
        warehouse = warehouse_dao.get_warehouse_by_id(warehouse_id)
        if warehouse:
            warehouse_dao.delete_warehouse_by_id(warehouse_id)
            if not warehouse_dao.get_warehouse_by_id(warehouse_id):
                return jsonify(message=f'Warehouse {warehouse_id} deleted successfully')
            else:
                return jsonify(error='Warehouse could not be deleted'), 404
        else:
            warehouse_dao.rollback()
            return jsonify(error='Warehouse not found'), 404

    except Exception as e:
        error_message = str(e)
        warehouse_dao.rollback()
        return jsonify(error=error_message), 500