import logging
import os

from flask import Flask, Response, request

from client.application.client import (PingCommand,
                                       PingWithContextProcessorCommand,
                                       GrpcChannel
                                       )
from protos.calculation_pb2 import FibonacciRequest

logger = logging.getLogger('client')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def landing():
    logger.debug(f"This is a test web app with a new deployment")
    return Response(f"This is a test web app with a new deployment")


@app.route('/ping', methods=['GET'])
def ping():
    channel = GrpcChannel(host=os.getenv('HOST', '0.0.0.0'),
                          port=int(os.getenv('PORT', 50051))
                          )
    command = PingCommand(grpc_channel=channel)
    response = command.execute()
    return Response(f'{response.message} from [{response.server_name}]')


@app.route('/ping-open-close', methods=['GET'])
def ping_with_context_processor():
    channel = GrpcChannel(host=os.getenv('HOST', '0.0.0.0'),
                          port=int(os.getenv('PORT', 50051))
                          )
    command = PingWithContextProcessorCommand(grpc_channel=channel)
    response = command.execute()
    return Response(f'{response.message} from [{response.server_name}]')

# @app.route('/fibo', methods=['GET'])
# def fibo():
#     fibo_client = ClientFactory().get_client()
#     number = int(request.args.get('number', 10))
#     response = fibo_client.Fibonacci(FibonacciRequest(number=number))
#     logger.debug(f"Number is {number},  response is {response.number} from node"
#                  f" {response.server_name}")
#     return Response(f"Fibonacci for {number} is {response.number} from node"
#                     f" {response.server_name}")
