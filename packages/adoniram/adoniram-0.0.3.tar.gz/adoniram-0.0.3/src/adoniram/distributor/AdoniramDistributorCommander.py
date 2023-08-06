from nehushtan.socket.NehushtanTCPSocketClient import NehushtanTCPSocketClient

from adoniram.SharedKit import adoniram_make_server_logger
from adoniram.message.request.RequestMessageAsShutdownServer import RequestMessageAsShutdownServer


class AdoniramDistributorCommander(NehushtanTCPSocketClient):

    def __init__(self, host: str, port: int, command: str):
        super().__init__(port, host)
        self.__command = command
        self.__logger = adoniram_make_server_logger(f'DistributorCommander')

    def handle_client_conneciton(self):
        if self.__command == 'ShutdownServer':
            request = RequestMessageAsShutdownServer().build('AdoniramDistributorCommander')
            sent = self.get_connection().send(request.get_message_as_bytes())
            self.__logger.info(f'handle_client_conneciton command: {request.get_message_dict()}', sent)

            response = self.get_connection().recv(4096)
            self.__logger.info(f'response: {response}')
        else:
            raise NotImplementedError()
