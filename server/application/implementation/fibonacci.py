import logging
import math

from decimal import Decimal

from xkcdpass import xkcd_password
from protos.calculation_pb2_grpc import CalculationsServicer
from protos.calculation_pb2 import FibonacciResponse, PingResponse


logger = logging.getLogger('server')


class FibonacciService(CalculationsServicer):
    def __init__(self):
        wordfile = xkcd_password.locate_wordfile()
        mywords = xkcd_password.generate_wordlist(wordfile=wordfile,
                                                  min_length=5,
                                                  max_length=8)
        self.name = xkcd_password.generate_xkcdpassword(mywords,
                                                        acrostic="server")

    def Ping(self, request, context):
        logger.debug(f"This is a ping request in action in {self.name}."
                     f"Service is Updated")
        return PingResponse(message="Service is updated properly.",
                            server_name=self.name)

    def Fibonacci(self, request, context):
        logger.debug(f"I'm calculating {request.number} in {self.name}")
        number = (
                (
                        (1 + math.sqrt(5)) ** request.number - (
                            1 - math.sqrt(5)) ** request.number
                )
                /
                ((2 ** request.number) * math.sqrt(5))
        )
        output = Decimal(number)
        logger.debug(f"Fibonacci {request.number} is {output}"
                     f".Service is updated.")
        return FibonacciResponse(number=output, server_name=self.name)
