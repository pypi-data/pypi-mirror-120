from adoniram.SharedKit import adoniram_get_shared_processor_registration
from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone


class RequestMessageAsRegisterProcessor(BaseRequestMessage):

    def __init__(self):
        super().__init__()

    def defined_request_action(self):
        return 'RegisterProcessor'

    def load_from_base_message(self, bm: BaseRequestMessage):
        self.set_message_dict(bm.get_message_dict())
        return self

    def get_processor_info(self):
        return self.read(('processor_info',))

    def handle_request_for_response(self) -> BaseResponseMessage:
        host = self.read(('processor_info', 'host'))
        port = self.read(('processor_info', 'port'))
        adoniram_get_shared_processor_registration().register(
            self.read_processor_name(), host, port
        )
        return ResponseMessageAsDone()
