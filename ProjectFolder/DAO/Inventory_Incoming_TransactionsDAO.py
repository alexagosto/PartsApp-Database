from DAO.dao import BaseDAO


class Inventory_Incoming_TransactionsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def create_transactions(self, part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, profit):
        query = 'INSERT INTO "Inventory_Incoming_Transactions" ("PartID", "SupplierID", "RackID", "WarehouseID", "UserID", "TransactionDate", "Profit") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING "TransactionID";'
        cur = self.execute_query(query, (part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, profit))
        self.commit()
        return cur.fetchone()

    def get_transactions(self):
        query = 'SELECT * FROM "Inventory_Incoming_Transactions";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_transactions_by_id(self, transaction_id):
        query = 'SELECT * FROM "Inventory_Incoming_Transactions" WHERE "TransactionID" = %s;'
        cur = self.execute_query(query, (transaction_id,))
        return cur.fetchone()

    def update_transactions_by_id(self, transaction_id, part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, profit):
        query = 'UPDATE "Inventory_Incoming_Transactions" Set "PartID" = %s, "SupplierID" = %s, "RackID" = %s, "WarehouseID" = %s, "UserID" = %s, "TransactionDate" = %s, "Profit" = %s WHERE "TransactionID" = %s;'
        self.execute_query(query, (part_id, supplier_id, rack_id, warehouse_id, user_id, transaction_date, profit, transaction_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()
