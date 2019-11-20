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
        options = (
                                 ('grpc.keepalive_time_ms', 10000),
                                 # send keepalive ping every 10 second, default is 2 hours
                                 ('grpc.keepalive_timeout_ms', 5000),
                                 # keepalive ping time out after 5 seconds, default is 20 seoncds
                                 ('grpc.keepalive_permit_without_calls', True),
                                 # allow keepalive pings when there's no gRPC calls
                                 ('grpc.http2.max_pings_without_data', 0),
                                 # allow unlimited amount of keepalive pings without data
                                 (
                                 'grpc.http2.min_time_between_pings_ms', 10000),
                                 # allow grpc pings from client every 10 seconds
                                 (
                                 'grpc.http2.min_ping_interval_without_data_ms',
                                 5000),
                                 # allow grpc pings from client without data every 5 seconds
                             )
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        listen = f'{host}:{port}'
        logger.debug(f"We will listen at {host}:{port}. Manual update..")
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
