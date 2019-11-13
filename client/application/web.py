import logging
import os

import grpc
import logconfig

from flask import Flask, Response, request
from pathlib import Path

from client.application.client import ClientFactory
from protos.calculation_pb2 import PingRequest, FibonacciRequest

logger = logging.getLogger('client')
app = Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    ping_client = ClientFactory.client()
    response = ping_client.Ping(PingRequest())
    logger.debug(f"Raw response is {response.message}")
    return Response(f'{response.message}')


@app.route('/fibo', methods=['GET'])
def fibo():
    fibo_client = ClientFactory.client()
    number = int(request.args.get('number', 10))
    response = fibo_client.Fibonacci(FibonacciRequest(number=number))
    logger.debug(f"Number is {number},  response is {response.number}")
    return Response(f"Fibonacci for {number} is {response.number}")
