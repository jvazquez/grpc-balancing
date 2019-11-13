FROM python:3.7.2
COPY client /grpc-balancing/client
COPY protos /grpc-balancing/protos
COPY requirements /grpc-balancing/requirements
WORKDIR /grpc-balancing
RUN pip install --upgrade pip && pip install -r requirements/requirements.txt
RUN python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. protos/*.proto
# Behind LB we are behind this
EXPOSE 8000
ENV GRPC_VERBOSITY=info
ENV FLASK_RUN_PORT=8000
CMD FLASK_APP=client/application/web.py
