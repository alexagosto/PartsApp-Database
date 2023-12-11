from DAO.dao import BaseDAO

class RacksDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

# first check if a warehouse with the given id exists
    def create_rack(self, rack_capacity, rack_quantity, rack_warehouse_id):
        query = 'INSERT INTO "Racks" ("RackCapacity", "RackQuantity", "WarehouseID") VALUES (%s, %s, %s) RETURNING "RackID";'
        cur = self.execute_query(query, (rack_capacity, rack_quantity, rack_warehouse_id,))
        self.commit()
        return cur.fetchone()

    def get_racks(self):
        query = 'SELECT * FROM "Racks"'
        cur = self.execute_query(query)
        return cur.fetchall()
    
    def get_rack_by_id(self, racks_id):
        query = 'SELECT * FROM "Racks" WHERE "RackID" = %s;'
        cur = self.execute_query(query, (racks_id,))
        return cur.fetchone()
    
    def get_racks_by_warehouse_id(self, warehouse_id):
        query = 'SELECT * FROM "Racks" WHERE "WarehouseID" = %s;'
        cur = self.execute_query(query, (warehouse_id,))
        return cur.fetchall()

    def update_rack_by_id(self, racks_id, new_rack_capacity, new_rack_quantity, new_rack_warehouse_id):
        query = 'UPDATE "Racks" Set "RackCapacity" = %s, "RackQuantity" = %s, "WarehouseID" = %s WHERE "RackID" = %s;'
        self.execute_query(query, (new_rack_capacity, new_rack_quantity, new_rack_warehouse_id, racks_id,))
        self.commit()

    def delete_rack_by_id(self, racks_id):
        query = 'DELETE FROM "Racks" Where "RackID" = %s;'
        self.execute_query(query, (racks_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()