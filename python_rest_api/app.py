import json

from flask import Flask, Response, request
from order_api.api import OrderApi
from product_api.api import ProductApi
from user_api.api import UserApi
from version import __version__

app = Flask(__name__)


@app.route("/health", methods=['GET'])
def check_health():
    response_body = json.dumps({"health": "OK"})
    return Response(response=response_body, status=200, content_type='application/json')


@app.route("/version", methods=['GET'])
def check_version():
    response_body = json.dumps({"version": __version__})
    return Response(response=response_body, status=200, content_type='application/json')


@app.route("/orders", methods=['GET'])
def list_all_orders():
    response = OrderApi({}).list()
    return Response(response=response['body'], status=response['status_code'], content_type='application/json')


@app.route("/orders", methods=['POST'])
def add_order():
    payload = request.get_json()
    response = OrderApi(payload).add()
    return Response(response=response['body'], status=response['status_code'], content_type='application/json')


@app.route("/products", methods=['GET'])
def list_all_products():
    response = ProductApi({}).list()
    return Response(response=response['body'], status=response['status_code'], content_type='application/json')


@app.route("/users", methods=['GET'])
def list_all_users():
    response = UserApi({}).list()
    return Response(response=response['body'], status=response['status_code'], content_type='application/json')


app.run(port=5000)
