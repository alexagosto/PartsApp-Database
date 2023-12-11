from DAO.dao import BaseDAO

class WarehousesDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def create_warehouse(self, warehouse_name, warehouse_address, warehouse_city, warehouse_budget):
        query = 'INSERT INTO "Warehouses" ("WarehouseName", "WarehouseAddress", "WarehouseCity", "Budget") VALUES (%s, %s, %s, %s) RETURNING "WarehouseID";'
        cur = self.execute_query(query, (warehouse_name, warehouse_address, warehouse_city, warehouse_budget))
        self.commit()
        return cur.fetchone()

    def get_warehouses(self):
        query = 'SELECT * FROM "Warehouses";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_warehouse_by_id(self, warehouseid):
        query = 'SELECT * FROM "Warehouses" WHERE "WarehouseID" = %s;'
        cur = self.execute_query(query, (warehouseid,))
        return cur.fetchone()

    def get_warehouse_by_warehouse_name(self, warehouse_name):
        query = 'SELECT * FROM "Warehouses" WHERE "WarehouseName" = %s;'
        cur = self.execute_query(query, (warehouse_name,))
        return cur.fetchall()

    def get_warehouse_by_warehouse_address(self, warehouse_address):
        query = 'SELECT * FROM "Warehouses" WHERE "WarehouseAddress" = %s;'
        cur = self.execute_query(query, (warehouse_address,))
        return cur.fetchall()

    def get_warehouse_by_warehouse_city(self, warehouse_city):
        query = 'SELECT * FROM "Warehouses" WHERE "WarehouseCity" = %s;'
        cur = self.execute_query(query, (warehouse_city,))
        return cur.fetchall()

    def update_warehouse_by_id(self, warehouse_id, warehouse_name, warehouse_address, warehouse_city, warehouse_budget):
        query = 'UPDATE "Warehouses" Set "WarehouseName" = %s, "WarehouseAddress" = %s, "WarehouseCity" = %s, "Budget" = %s WHERE "WarehouseID" = %s;'
        self.execute_query(query, (warehouse_name, warehouse_address, warehouse_city, warehouse_budget, warehouse_id))
        self.commit()

    def delete_warehouse_by_id(self, warehouse_id):
        query = 'DELETE FROM "Warehouses" Where "WarehouseID" = %s;'
        self.execute_query(query, (warehouse_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()