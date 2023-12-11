from DAO.dao import BaseDAO

class UsersDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)
    def create_user(self, username, warehouseid, user_email):
        query = 'INSERT INTO "Users" ("Username", "WarehouseID", "UserEmail") VALUES (%s, %s, %s) RETURNING "UserID";'
        cur = self.execute_query(query, (username, warehouseid, user_email))
        self.commit()
        return cur.fetchone()

    def get_users(self):
        query = 'SELECT * FROM "Users";'
        cur = self.execute_query(query)
        return cur.fetchall()

    def get_user_by_id(self, user_id):
        query = 'SELECT * FROM "Users" WHERE "UserID" = %s;'
        cur = self.execute_query(query,(user_id,))
        return cur.fetchone()

    def get_user_by_username(self, username):
        query = 'SELECT * FROM "Users" WHERE "Username" = %s;'
        cur = self.execute_query(query, (username,))
        return cur.fetchall

    def get_users_by_warehouse(self, warehouseid):
        query = 'SELECT * FROM "Users" WHERE "WarehouseID" = %s;'
        cur = self.execute_query(query, (warehouseid,))
        return cur.fetchall()

    def update_user_by_id(self, user_id, new_username, new_warehouse, new_email):
        query = 'UPDATE "Users" Set "Username" = %s, "WarehouseID" = %s, "UserEmail" = %s WHERE "UserID" = %s;'
        self.execute_query(query, (new_username, new_warehouse, new_email, user_id))
        self.commit()

    def delete_user_by_id(self, user_id):
        query = 'DELETE FROM "Users" WHERE "UserID" = %s;'
        self.execute_query(query, (user_id,))
        self.commit()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()