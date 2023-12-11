from DAO.dao import BaseDAO


class Outgoing_Transaction_ReceiversDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def create_receivers(self, receiver_name):
        query = 'INSERT INTO "Outgoing_Transaction_Receiver" ("ReceiverName") VALUES (%s, %s, %s) RETURNING "ReceiverID";'
        cur = self.execute_query(query, (receiver_name,))
        self.commit()
        return cur.fetchone()

    def get_receivers(self):
        query = 'SELECT * FROM "Outgoing_Transaction_Receiver";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_receivers_by_id(self, receiver_id):
        query = 'SELECT * FROM "Outgoing_Transaction_Receiver" WHERE "ReceiverID" = %s;'
        cur = self.execute_query(query, (receiver_id,))
        return cur.fetchone()

    def update_receivers_by_id(self, receiver_id, receiver_name):
        query = 'UPDATE "Outgoing_Transaction_Receiver" Set "ReceiverName" = %s WHERE "ReceiverID" = %s;'
        self.execute_query(query, (receiver_name, receiver_id))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()