from flask import Blueprint, request, jsonify
from DAO.dao_factory import DAOFactory
from config.connectHeroku import conn

supplier_handler = Blueprint('supplier_handler', __name__)


@supplier_handler.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()
    supplier_name = data.get('SupplierName')
    supplier_address = data.get('SupplierAddress')
    supplier_city = data.get('SupplierCity')

    dao_factory = DAOFactory(conn)
    supplier_dao = dao_factory.get_suppliers_dao()

    try:
        supplier_id = supplier_dao.create_suppliers(supplier_name, supplier_address, supplier_city)
        response = {
            'message': 'Supplier created successfully',
            'SupplierID': supplier_id[0]
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = str(e)
        supplier_dao.rollback()
        return jsonify(error=error_message), 500


@supplier_handler.route('/', methods=['GET'])
def get_suppliers():
    dao_factory = DAOFactory(conn)
    suppliers_dao = dao_factory.get_suppliers_dao()

    suppliers = suppliers_dao.get_suppliers()

    try:
        response = []
        for supplier in suppliers:
            supplier_data = {
                'supplier_id': supplier[3],
                'supplier_name': supplier[0],
                'supplier_address': supplier[1],
                'supplier_city': supplier[2]
            }
            response.append(supplier_data)

        return jsonify(response)

    except Exception as e:
        error_message = str(e)
        suppliers_dao.rollback()
        return jsonify(error=error_message), 500


@supplier_handler.route('/<int:supplier_id>', methods=['GET'])
def get_supplier_by_id(supplier_id):
    dao_factory = DAOFactory(conn)
    suppliers_dao = dao_factory.get_suppliers_dao()

    try:
        suppliers = suppliers_dao.get_suppliers_by_id(supplier_id)
        if suppliers:
            response = {
                'supplier_id': suppliers[3],
                'supplier_name': suppliers[0],
                'supplier_address': suppliers[1],
                'supplier_city': suppliers[2]
            }

            return jsonify(response)
        else:
            suppliers_dao.rollback()
            return jsonify(error='Supplier not found'), 404

    except Exception as e:
        error_message = str(e)
        suppliers_dao.rollback()
        return jsonify(error=error_message), 500


@supplier_handler.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    data = request.get_json()
    new_suppliername = data.get('SupplierName')
    new_supplieraddress = data.get('SupplierAddress')
    new_suppliercity = data.get('SupplierCity')
    dao_factory = DAOFactory(conn)
    suppliers_dao = dao_factory.get_suppliers_dao()

    try:
        suppliers_dao.update_suppliers_by_id(supplier_id, new_suppliername, new_supplieraddress, new_suppliercity)
        supplier = suppliers_dao.get_suppliers_by_id(supplier_id)
        if supplier and (
                supplier[0] == new_suppliername and
                supplier[1] == new_supplieraddress and
                supplier[2] == new_suppliercity
        ):
            return jsonify(message=f'Supplier {supplier_id} updated successfully')

        else:
            suppliers_dao.rollback()
            return jsonify(error='Supplier not found'), 404

    except Exception as e:
        error_message = str(e)
        suppliers_dao.rollback()
        return jsonify(error=error_message), 500


@supplier_handler.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    dao_factory = DAOFactory(conn)
    suppliers_dao = dao_factory.get_suppliers_dao()

    try:
        supplier = suppliers_dao.get_suppliers_by_id(supplier_id)
        if supplier:
            suppliers_dao.delete_suppliers_by_id(supplier_id)
            if not suppliers_dao.get_suppliers_by_id(supplier_id):
                return jsonify(message=f'Supplier {supplier_id} deleted successfully')
            else:
                return jsonify(error='Supplier not found'), 404
        else:
            suppliers_dao.rollback()
            return jsonify(error='Supplier not found'), 404

    except Exception as e:
        error_message = str(e)
        suppliers_dao.rollback()
        return jsonify(error=error_message), 500