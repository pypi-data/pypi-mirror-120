from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone


class RequestMessageAsPing(BaseRequestMessage):

    def __init__(self):
        super().__init__()

    def defined_request_action(self):
        return 'Ping'

    def handle_request_for_response(self) -> BaseResponseMessage:
        return ResponseMessageAsDone()
