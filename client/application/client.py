import logging
import os

import grpc
import logconfig

from pathlib import Path

from protos.calculation_pb2_grpc import CalculationsStub

logging_configuration_file = Path(__file__) \
    .joinpath('../../configuration/logging.json').resolve()
logconfig.from_json(logging_configuration_file.resolve())
logger = logging.getLogger('client')


class ClientFactory:
    @staticmethod
    def client():
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 50051))
        channel = grpc.insecure_channel(f'{host}:{port}')
        logger.debug(f"We will use channel {host}:{port}")
        return CalculationsStub(channel)
