import logging
import os

import grpc
import logconfig

from concurrent import futures
from pathlib import Path

from protos.calculation_pb2_grpc import add_CalculationsServicer_to_server
from server.application.implementation.fibonacci import FibonacciService

logger = logging.getLogger('server')


def server(host, port, **kwargs):
    """
    Runs the main GRPC server
    :param host:
    :param port:
    :param kwargs:
    :return:
    """
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        listen = f'{host}:{port}'
        logger.debug(f"We will listen at {host}:{port}")
        server.add_insecure_port(listen)
        add_CalculationsServicer_to_server(
            FibonacciService(), server)
        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Interruption detected, closing")


if __name__ == "__main__":
    logging_configuration_file = Path(__file__)\
        .joinpath('../../configuration/logging.json').resolve()
    logconfig.from_json(logging_configuration_file.resolve())
    server(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 50051))
    )
