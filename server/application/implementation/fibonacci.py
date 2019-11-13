import logging
import math

from decimal import Decimal, ROUND_UP

from protos.calculation_pb2_grpc import CalculationsServicer
from protos.calculation_pb2 import FibonacciResponse, PingResponse

logger = logging.getLogger('server')


class FibonacciService(CalculationsServicer):
    def Ping(self, request, context):
        logger.debug("This is a ping request in action")
        return PingResponse(message="Service is alive")

    def Fibonacci(self, request, context):
        logger.debug(f"I'm calculating {request.number}")
        number = (
                (
                        (1 + math.sqrt(5)) ** request.number - (
                            1 - math.sqrt(5)) ** request.number
                )
                /
                ((2 ** request.number) * math.sqrt(5))
        )
        output = Decimal(number)
        logger.debug(f"Fibonacci {request.number} is {output}")
        return FibonacciResponse(number=output)
