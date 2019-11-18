import logging

from flask import Flask, Response, request

from client.application.client import ClientFactory
from protos.calculation_pb2 import PingRequest, FibonacciRequest

logger = logging.getLogger('client')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def landing():
    logger.debug(f"This is a test web app with a new deployment")
    return Response(f"This is a test web app with a new deployment")


@app.route('/ping', methods=['GET'])
def ping():
    ping_client = ClientFactory.client()
    response = ping_client.Ping(PingRequest())
    logger.debug(f"Raw response is {response.message} from node"
                 f"{response.server_name}")
    return Response(f'{response.message} from [{response.server_name}]')


@app.route('/fibo', methods=['GET'])
def fibo():
    fibo_client = ClientFactory.client()
    number = int(request.args.get('number', 10))
    response = fibo_client.Fibonacci(FibonacciRequest(number=number))
    logger.debug(f"Number is {number},  response is {response.number} from node"
                 f" {response.server_name}")
    return Response(f"Fibonacci for {number} is {response.number} from node"
                    f" {response.server_name}")
