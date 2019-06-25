from flask import Flask, Response, json
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


app.run(port=5000)
