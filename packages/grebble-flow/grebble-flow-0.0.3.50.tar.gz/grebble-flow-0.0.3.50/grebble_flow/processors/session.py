from grebble_flow.transport.generated.sdk.v1.processor_pb2 import Message


class Session:
    def __init__(self, msg: Message):
        self.msg = msg

    def get_message(self):
        return self.msg
