from DAO.dao import BaseDAO


class TransactionsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def create_transactions(self, user_id, transaction_date, transaction_profit):
        query = 'INSERT INTO "Transactions" ("UserID", "TransactionDate", "Profit") VALUES (%s, %s, %s) RETURNING "TransactionID";'
        cur = self.execute_query(query, (user_id, transaction_date, transaction_profit,))
        self.commit()
        return cur.fetchone()

    def get_transactions(self):
        query = 'SELECT * FROM "Transactions";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_transactions_by_id(self, transaction_id):
        query = 'SELECT * FROM "Transactions" WHERE "TransactionID" = %s;'
        cur = self.execute_query(query, (transaction_id,))
        return cur.fetchone()

    def update_transactions_by_id(self, transaction_id, user_id, transaction_date, transaction_profit):
        query = 'UPDATE "Transactions" Set "UserID" = %s, "TransactionDate" = %s, "Profit" = %s WHERE "TransactionID" = %s;'
        self.execute_query(query, (user_id, transaction_date, transaction_profit, transaction_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()
