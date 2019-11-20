import logging
import os

import grpc
import logconfig

from abc import ABC, abstractmethod
from pathlib import Path

from protos.calculation_pb2_grpc import CalculationsStub
from protos.calculation_pb2 import PingRequest, FibonacciRequest

logging_configuration_file = Path(__file__) \
    .joinpath('../../configuration/logging.json').resolve()
logconfig.from_json(logging_configuration_file.resolve())
logger = logging.getLogger('client')


class GrpcCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class GrpcChannel:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        logger.debug(f"Host: {host}. Port: {port}")


class PingCommand(GrpcCommand):
    def __init__(self, grpc_channel: GrpcChannel):
        self.connection_string = f'{grpc_channel.host}:{grpc_channel.port}'

    def execute(self):
        response = None
        try:
            channel = grpc.insecure_channel(self.connection_string)
            ping_client = CalculationsStub(channel)
            response = ping_client.Ping(PingRequest())
        except Exception:
            logger.exception("Error trying to execute ping command")

        return response


class PingWithContextProcessorCommand(GrpcCommand):
    def __init__(self, grpc_channel: GrpcChannel):
        self.connection_string = f'{grpc_channel.host}:{grpc_channel.port}'

    def execute(self):
        response = None
        try:
            # We are behind a NLB, the lb_policy_name is a bit weird
            channel_options = [
                ("grpc.keepalive_timeout_ms", 10000),
                ('grpc.lb_policy_name', 'pick_first'),
                ("grpc.keepalive_timeout_ms", 5000),
                ('grpc.keepalive_permit_without_calls', True),
                ('grpc.http2.max_pings_without_data', 0),
                ('grpc.http2.min_time_between_pings_ms', 10000),
                ('grpc.http2.min_ping_interval_without_data_ms', 5000)
            ]
            with grpc.insecure_channel(self.connection_string,
                                       options=channel_options) as channel:
                ping_client = CalculationsStub(channel)
                response = ping_client.Ping(PingRequest())
        except Exception:
            logger.exception("Error trying to execute ping command")

        return response
