import logging
from concurrent import futures

import grpc
from grebble_flow.transport.generated.sdk.v1 import processor_pb2_grpc
from grebble_flow.transport.service.processor import ProcessorService


def start_server(port):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
        ],
    )
    processor_pb2_grpc.add_ProcessorServiceServicer_to_server(
        ProcessorService(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Server started")
    server.wait_for_termination()
