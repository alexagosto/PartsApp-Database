from .PartsDAO import PartsDAO
from .RacksDAO import RacksDAO
from .UsersDAO import UsersDAO
from .WarehousesDAO import WarehousesDAO
from .SuppliersDAO import SuppliersDAO
from .TransactionsDAO import TransactionsDAO
from .Inventory_Incoming_TransactionsDAO import Inventory_Incoming_TransactionsDAO
from .Inventory_Outgoing_TransactionsDAO import Inventory_Outgoing_TransactionsDAO
from .Inventory_Transfer_TransactionsDAO import Inventory_Transfer_TransactionsDAO
from .Outgoing_Transaction_ReceiversDAO import Outgoing_Transaction_ReceiversDAO
from .Local_Statistics_DAO import LocalStatisticsDAO
from .Most_Global_Statistics_DAO import MostGlobalStatisticsDAO
from .Least_Global_Statistics_DAO import LeastGlobalStatisticsDAO
from .front_statsDAO import FrontStatsDAO


class DAOFactory:
    def __init__(self, conn):
        self.conn = conn

    def get_parts_dao(self):
        return PartsDAO(self.conn)

    def get_racks_dao(self):
        return RacksDAO(self.conn)

    def get_users_dao(self):
        return UsersDAO(self.conn)

    def get_warehouses_dao(self):
        return WarehousesDAO(self.conn)

    def get_suppliers_dao(self):
        return SuppliersDAO(self.conn)

    def get_transactions_dao(self):
        return TransactionsDAO(self.conn)

    def get_inventory_incoming_transactions_dao(self):
        return Inventory_Incoming_TransactionsDAO(self.conn)

    def get_inventory_outgoing_transactions_dao(self):
        return Inventory_Outgoing_TransactionsDAO(self.conn)

    def get_inventory_transfer_transactions_dao(self):
        return Inventory_Transfer_TransactionsDAO(self.conn)

    def get_outgoing_transaction_receivers_dao(self):
        return Outgoing_Transaction_ReceiversDAO(self.conn)

    def get_local_statistics_dao(self):
        return LocalStatisticsDAO(self.conn)

    def get_most_global_statistics_dao(self):
        return MostGlobalStatisticsDAO(self.conn)

    def get_least_global_statistics_dao(self):
        return LeastGlobalStatisticsDAO(self.conn)

    def get_front_stats_dao(self):
        return FrontStatsDAO(self.conn)