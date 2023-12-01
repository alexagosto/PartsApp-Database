from DAO.dao import BaseDAO


class FrontStatsDAO(BaseDAO):
    def __init__(self, conn):
        super().__init__(conn)

    def get_all_transactions(self, warehouse_id):
        query = '''SELECT *
                    FROM (
                        SELECT "TransactionID", "UserID", "TransactionDate", "Profit"
                        FROM "Inventory_Transfer_Transactions"
                        WHERE "UserID" IN (
                            SELECT "UserID"
                            FROM "Users"
                            WHERE "WarehouseID" = %s
                        )
                        UNION ALL
                        SELECT "TransactionID", "UserID", "TransactionDate", "Profit"
                        FROM "Inventory_Incoming_Transactions"
                        WHERE "UserID" IN (
                            SELECT "UserID"
                            FROM "Users"
                            WHERE "WarehouseID" = %s
                        )  
                        UNION ALL
                        SELECT "TransactionID", "UserID", "TransactionDate", "Profit"
                        FROM "Inventory_Outgoing_Transactions"
                        WHERE "UserID" IN (
                            SELECT "UserID"
                            FROM "Users"
                            WHERE "WarehouseID" = %s
                        )
                    ) AS combined_transactions
                    ORDER BY "TransactionDate" DESC;'''
        cur = self.execute_query(query, (warehouse_id, warehouse_id, warehouse_id))
        self.commit()
        return cur.fetchall()

    def get_all_parts_by_supplier(self, supplier_id):
        query = '''Select "PartID", "PartName", "PartPrice", "PartType"
                    from "Parts" natural join "Parts_Suppliers" natural join "Suppliers"
                    Where "SupplierID" = %s
                    ORDER BY "PartID"'''
        cur = self.execute_query(query, (supplier_id,))
        self.commit()
        return cur.fetchall()

    def get_all_parts_by_warehouse(self, warehouse_id):
        query = '''Select "PartID", "PartName", "PartPrice", "PartType"
                    from "Parts" natural join "Racks_Parts" natural join "Racks"
                    Where "WarehouseID" = %s
                    ORDER BY "PartID"'''
        cur = self.execute_query(query, (warehouse_id,))
        self.commit()
        return cur.fetchall()

    def get_all_part_prices(self):
        query = '''Select *
                    From "Parts"
                    ORDER BY "PartID"'''
        cur = self.execute_query(query)
        self.commit()
        return cur.fetchall()

    def rollback(self):
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        self.conn.commit()

