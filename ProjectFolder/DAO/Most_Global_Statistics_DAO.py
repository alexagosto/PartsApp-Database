from DAO.dao import BaseDAO


class MostGlobalStatisticsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def get_most_rack(self):
        query = '''Select "WarehouseID", "WarehouseName", count("RackID") as count
            From "Warehouses" natural join "Racks"
            GROUP BY "WarehouseID", "WarehouseName"
            ORDER BY count desc
            Limit 10;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def get_most_incoming(self):
        query = '''Select "WarehouseID", "WarehouseName", count("TransactionID") as count
            FROM "Inventory_Incoming_Transactions" natural join "Warehouses"
            Group by "WarehouseID", "WarehouseName"
            Order by count desc
            Limit 5;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def get_most_deliver(self):
        query = '''Select "WarehouseID", "WarehouseName", count("TransactionID") as count
            FROM "Inventory_Transfer_Transactions" join "Warehouses" on "WarehouseID"="SourceWarehouseID"
            Group by "WarehouseID", "WarehouseName"
            Order by count desc
            Limit 5;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def get_most_transactions(self):
        query = '''SELECT combined_transactions."UserID", "Username", COUNT(DISTINCT combined_transactions."TransactionID") AS count
                    FROM (
                        SELECT "UserID", "TransactionID" FROM "Inventory_Transfer_Transactions"
                        UNION ALL
                        SELECT "UserID", "TransactionID" FROM "Inventory_Incoming_Transactions"
                        UNION ALL
                        SELECT "UserID", "TransactionID" FROM "Inventory_Outgoing_Transactions"
                    ) AS combined_transactions
                    JOIN "Users" ON combined_transactions."UserID" = "Users"."UserID"
                    GROUP BY combined_transactions."UserID", "Username"
                    ORDER BY count DESC
                        LIMIT 3;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def get_most_city(self):
        query = '''SELECT "WarehouseCity", COUNT("TransactionID") AS count
                    FROM (
                        SELECT "TransactionID", "UserID"
                        FROM "Inventory_Transfer_Transactions"
                        UNION ALL
                        SELECT "TransactionID", "UserID"
                        FROM "Inventory_Incoming_Transactions"
                        UNION ALL
                        SELECT "TransactionID", "UserID"
                        FROM "Inventory_Outgoing_Transactions"
                    ) AS combined_transactions
                    JOIN "Users" ON combined_transactions."UserID" = "Users"."UserID"
                    JOIN "Warehouses" ON "Users"."WarehouseID" = "Warehouses"."WarehouseID"
                    GROUP BY "WarehouseCity"
                    ORDER BY count DESC
                    LIMIT 3;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()
