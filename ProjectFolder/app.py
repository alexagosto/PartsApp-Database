from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_cors import CORS, cross_origin
from Handlers.parts_handler import parts_handler
from Handlers.racks_handler import racks_handler
from Handlers.users_handler import user_handler
from Handlers.warehouses_handler import warehouse_handler
from Handlers.suppliers_handler import supplier_handler
from Handlers.transactions_handler import transaction_handler
from Handlers.inventory_incoming_transactions_handler import inventory_incoming_transaction_handler
from Handlers.inventory_outgoing_transactions_handler import inventory_outgoing_transaction_handler
from Handlers.inventory_transfer_transaction_handler import inventory_transfer_transaction_handler
from Handlers.outgoing_transaction_reciever_handler import outgoing_transaction_receiver_handler
from Handlers.local_statistics_handler import local_statistics_handler
from Handlers.least_global_statistics_handler import least_global_statistics_handler
from Handlers.most_global_statistics_handler import most_global_statistics_handler
from Handlers.front_stats_handler import front_stats_handler


app = Flask(__name__)
# Apply CORS to this app
CORS(app)


app.register_blueprint(parts_handler, url_prefix='/jemsa/part')
app.register_blueprint(racks_handler, url_prefix='/jemsa/rack')
app.register_blueprint(user_handler, url_prefix='/jemsa/user')
app.register_blueprint(warehouse_handler, url_prefix='/jemsa/warehouse')
app.register_blueprint(supplier_handler, url_prefix='/jemsa/supplier')
app.register_blueprint(transaction_handler, url_prefix='/jemsa/transactions')
app.register_blueprint(inventory_incoming_transaction_handler, url_prefix='/jemsa/incoming')
app.register_blueprint(inventory_outgoing_transaction_handler, url_prefix='/jemsa/outgoing')
app.register_blueprint(inventory_transfer_transaction_handler, url_prefix='/jemsa/exchange')
app.register_blueprint(outgoing_transaction_receiver_handler, url_prefix='/jemsa/receivers')
# Similar route to warehouses, but meant for local statistics.
app.register_blueprint(local_statistics_handler, url_prefix='/jemsa/warehouse')
app.register_blueprint(most_global_statistics_handler, url_prefix='/jemsa/most')
app.register_blueprint(least_global_statistics_handler, url_prefix='/jemsa/least')
app.register_blueprint(front_stats_handler, url_prefix='/jemsa/frontstats')



if __name__ == '__main__':
    app.run(debug=True)