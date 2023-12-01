from DAO.dao import BaseDAO

class LocalStatisticsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def get_warehouse_profit(self, warehouse_id):
        query = '''SELECT "WarehouseID", sum(combined_data.profit) as net_profit, extract(YEAR FROM "TransactionDate") AS year
                 FROM(SELECT "WarehouseID", "Profit" as profit, "TransactionDate"
                 FROM "Inventory_Incoming_Transactions"
                 UNION ALL
                 SELECT "WarehouseID", "Profit" as profit, "TransactionDate"
                 FROM "Inventory_Outgoing_Transactions")
                 AS combined_data
                 Where "WarehouseID" = %s
                 GROUP BY year, "WarehouseID"
                 ORDER BY year desc ;'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()

    def get_rack_lowstock(self, warehouse_id):
        query = '''SELECT "RackID", (("RackQuantity"/"RackCapacity")) as capacity_percent
        From "Racks"
        Where (("RackQuantity"/"RackCapacity")) < 0.25 and "WarehouseID" = %s
        Order by "capacity_percent" desc
        Limit 5;'''
        cur = self.execute_query(query, (warehouse_id,))
        return cur.fetchall()

    def get_rack_material(self, warehouse_id):
        # This query gets the count of part types in a warehouse and displays the bottom 3 materials in quantity
        query = '''SELECT  count("PartType") as count, "PartType"
            FROM "Parts" natural join "Racks_Parts" natural join "Racks"
            WHERE "WarehouseID" = %s
            GROUP BY "PartType"
            ORDER BY count
            limit 3;'''

        # #This query gets the bottom 3 parts per price, and their type without grouping
        # second_query = '''SELECT  "PartType", "PartName", min("PartPrice")
        #     FROM "Parts" natural join "Racks_Parts" natural join "Racks"
        #     WHERE "WarehouseID" = %s
        #     GROUP BY "PartType", "PartName"
        #     ORDER BY min("PartPrice")
        #     limit 3;'''

        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()

    def get_rack_expensive(self, warehouse_id):
        query = '''SELECT "RackID", sum("PartPrice") as Total_Price
            FROM "Racks" natural join "Racks_Parts" natural join "Parts"
            Where "WarehouseID" = %s
            Group by "WarehouseID", "RackID"
            ORDER BY Total_Price desc
            Limit 5;'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()


    def get_transaction_suppliers(self, warehouse_id):
        query = '''SELECT "SupplierID", count("TransactionID") as count
            FROM "Suppliers" natural join "Inventory_Incoming_Transactions"
            Where "WarehouseID" = %s
            Group by "SupplierID"
            ORDER BY count desc
            Limit 3;'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()

    def get_transaction_leastcost(self, warehouse_id):
        query = '''SELECT  "TransactionDate", "Profit"
            FROM "Inventory_Incoming_Transactions"
            Where "WarehouseID" = %s
            ORDER BY "Profit" desc
            Limit 3;'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()


    def get_users_receivesmost(self, warehouse_id):
        query = '''Select "UserID", "Username", count("TransactionID") as count
            FROM "Users" natural join "Inventory_Transfer_Transactions"
            Where "WarehouseID" = %s
            Group by "UserID", "Username"
            ORDER BY count desc
            Limit 3;'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()