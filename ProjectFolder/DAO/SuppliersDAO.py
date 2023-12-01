from DAO.dao import BaseDAO


class SuppliersDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def create_suppliers(self, supplier_name, supplier_address, supplier_city):
        query = 'INSERT INTO "Suppliers" ("SupplierName", "SupplierAddress", "SupplierCity") VALUES (%s, %s, %s) RETURNING "SupplierID";'
        cur = self.execute_query(query, (supplier_name, supplier_address, supplier_city,))
        self.commit()
        return cur.fetchone()

    def get_suppliers(self):
        query = 'SELECT * FROM "Suppliers";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_suppliers_by_id(self, supplier_id):
        query = 'SELECT * FROM "Suppliers" WHERE "SupplierID" = %s;'
        cur = self.execute_query(query, (supplier_id,))
        return cur.fetchone()

    def update_suppliers_by_id(self, supplier_id, supplier_name, supplier_address, supplier_city):
        query = 'UPDATE "Suppliers" Set "SupplierName" = %s, "SupplierAddress" = %s, "SupplierCity" = %s WHERE "SupplierID" = %s;'
        self.execute_query(query, (supplier_name, supplier_address, supplier_city, supplier_id,))
        self.commit()

    def delete_suppliers_by_id(self, supplier_id):
        query = 'DELETE FROM "Suppliers" Where "SupplierID" = %s;'
        self.execute_query(query, (supplier_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()