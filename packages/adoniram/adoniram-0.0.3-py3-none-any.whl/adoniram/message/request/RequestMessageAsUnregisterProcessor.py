from adoniram.SharedKit import adoniram_get_shared_processor_registration
from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone


class RequestMessageAsUnregisterProcessor(BaseRequestMessage):

    def __init__(self):
        super().__init__()

    def defined_request_action(self):
        return 'UnregisterProcessor'

    def handle_request_for_response(self) -> BaseResponseMessage:
        adoniram_get_shared_processor_registration().unregister(self.read_processor_name())
        return ResponseMessageAsDone()
