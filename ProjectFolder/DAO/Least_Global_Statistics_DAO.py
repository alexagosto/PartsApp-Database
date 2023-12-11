from DAO.dao import BaseDAO


class LeastGlobalStatisticsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def get_least_outgoing(self):
        query = '''Select "WarehouseID", "WarehouseName", count("TransactionID") as count
            From "Warehouses" natural join "Inventory_Outgoing_Transactions"
            Group by "WarehouseID", "WarehouseName"
            Order by count
            limit 3;'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()