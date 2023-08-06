from adoniram.SharedKit import adoniram_get_shared_processor_registration
from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone


class RequestMessageAsShutdownServer(BaseRequestMessage):
    def defined_request_action(self):
        return 'ShutdownServer'

    def handle_request_for_response(self) -> BaseResponseMessage:
        adoniram_get_shared_processor_registration().stop_distributor_server()
        adoniram_get_shared_processor_registration()
        return ResponseMessageAsDone()
