import json
from abc import abstractmethod
from typing import Optional

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger
from nehushtan.logger.NehushtanLogging import NehushtanLogging
from nehushtan.socket.NehushtanTCPSocketClient import NehushtanTCPSocketClient

from adoniram.SharedKit import adoniram_make_server_logger
from adoniram.exception.BadMessageError import BadMessageError
from adoniram.exception.ServerConnectionLost import ServerConnectionLost
from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.request.RequestMessageAsRegisterProcessor import RequestMessageAsRegisterProcessor
from adoniram.message.request.RequestMessageAsUnregisterProcessor import RequestMessageAsUnregisterProcessor
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone


class AdoniramProcesserClient(NehushtanTCPSocketClient):

    def __init__(self, host: str, port: int, name: str):
        super().__init__(port, host)
        self.__processor_name = name
        self.__logger: NehushtanFileLogger = adoniram_make_server_logger(f'Processor-{name}')
        self.__registered = False

        # local debug
        self.__logger.print_higher_than_this_level = NehushtanLogging.INFO

    def get_logger(self):
        return self.__logger

    def get_processor_name(self):
        return self.__processor_name

    def _prepare_next_request(self) -> Optional[BaseRequestMessage]:
        """
        Return None to stop client recycle!
        1. register
        2. ping
        3. unregister (return None)
        :return:
        """

        if not self.__registered:
            return RequestMessageAsRegisterProcessor().build(self.__processor_name)
        else:
            while not self.should_processer_stop():
                return self.make_request_for_seeking_next_task_from_server()

    @abstractmethod
    def make_request_for_seeking_next_task_from_server(self) -> BaseRequestMessage:
        """
        Send a special request to server, try to get a task to do
        :return:
        """
        pass

    @abstractmethod
    def should_processer_stop(self) -> bool:
        """
        Processer should tell server to unregister now?
        :return:
        """
        pass

    def _handle_response(self, response_message: BaseResponseMessage):
        if response_message.read_code() == ResponseMessageAsDone.CODE:
            # Done
            if not self.__registered:
                self.__registered = True
                self.__logger.notice('PROCESSOR REGISTERED')
            else:
                self.handle_server_response_for_task_done(response_message)
                # other, ping
                # self.__logger.notice('PONG!')
        else:
            # error
            self.__logger.error('REQUEST FAILED', response_message.read(('data',)))

    @abstractmethod
    def handle_server_response_for_task_done(self, response_message: BaseResponseMessage):
        """
        When a task is done by server (no matter error or not)
        :param response_message:
        :return:
        """
        pass

    def handle_client_conneciton(self):
        while True:
            request = self._prepare_next_request()

            if not request:
                self.__logger.notice("handle_client_conneciton prepared None as unregister processor request")
                # request = RequestMessageAsPing().build(self.__processor_name)
                request = RequestMessageAsUnregisterProcessor().build(self.__processor_name)
                self.__logger.info('handle_client_conneciton prepared request', request.get_message_dict())
                sent = self.get_connection().send(request.get_message_as_bytes())
                self.__logger.info('handle_client_conneciton sent bytes', sent)
                received = self.get_connection().recv(4096)
                self.__logger.info(f'handle_client_conneciton receive unregister {received}')
                self.get_connection().close()
                return

            self.__logger.info('handle_client_conneciton prepared request', request.get_message_dict())
            sent = self.get_connection().send(request.get_message_as_bytes())
            self.__logger.info('handle_client_conneciton sent bytes', sent)

            received = b''
            base_message = BaseResponseMessage('')

            server_connection_lost = False
            while True:
                buffer = self.get_connection().recv(4096)
                if len(buffer) <= 0:
                    # connection lost
                    self.__logger.error('handle_client_conneciton received empty buffer, connection may be lost')
                    server_connection_lost = True

                received += buffer
                try:
                    base_message.load(received)
                    break
                except json.decoder.JSONDecodeError:
                    # the json string is not end yet
                    if server_connection_lost:
                        # so cannot fetch entire json
                        raise ServerConnectionLost()

            self.__logger.info(f'handle_client_conneciton received response json: {received}')

            # now base_message loaded

            code = base_message.read_code()
            self.__logger.info('handle_client_conneciton response code', code)
            response_message_for_code_class_name = 'ResponseMessageAs' + code
            self.__logger.info('handle_client_conneciton response_message_for_code_class_name',
                               response_message_for_code_class_name)
            response_message_for_code_class = CommonHelper.class_with_class_path(
                'adoniram.message.response.' + response_message_for_code_class_name
            )
            self.__logger.info(
                f'handle_client_conneciton response_message_for_code_class {response_message_for_code_class}')

            if not issubclass(BaseResponseMessage.__class__, response_message_for_code_class.__class__):
                raise BadMessageError('Unsupported Resposne Code', received)

            response_message_for_code = response_message_for_code_class()
            response_message_for_code.set_message_dict(base_message.get_message_dict())

            self._handle_response(response_message_for_code)
