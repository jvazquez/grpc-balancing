FROM python:3.7.2
COPY server /grpc-balancing/server
COPY protos /grpc-balancing/protos
COPY requirements /grpc-balancing/requirements
WORKDIR /grpc-balancing
RUN pip install --upgrade pip && pip install -r requirements/requirements.txt
RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. protos/*.proto
# Behind LB we are behind this
EXPOSE 50051
ENV GRPC_VERBOSITY=info
CMD python -m server.application.server
