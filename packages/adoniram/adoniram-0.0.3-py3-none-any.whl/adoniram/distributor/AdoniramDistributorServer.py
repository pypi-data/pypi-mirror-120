import json
import socket
import threading

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.socket.NehushtanTCPSocketServer import NehushtanTCPSocketServer

from adoniram.SharedKit import adoniram_get_shared_processor_registration, adoniram_make_server_logger
from adoniram.exception.BadMessageError import BadMessageError
from adoniram.exception.HandleMessageError import HandleMessageError
from adoniram.exception.ProcessorConnectionLost import ProcessorConnectionLost
from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.request.RequestMessageAsShutdownServer import RequestMessageAsShutdownServer
from adoniram.message.response.ResponseMessageAsRequestFormatError import ResponseMessageAsRequestFormatError
from adoniram.message.response.ResponseMessageAsRequestHandleError import ResponseMessageAsRequestHandleError


class AdoniramDistributorServer(NehushtanTCPSocketServer):

    def __init__(self, port: int):
        super().__init__(port)

        self.__logger = adoniram_make_server_logger(f'Distributor')

    def should_terminate(self) -> bool:
        self.__logger.info('CURRENT THREADS', {'total': threading.active_count()})

        x = adoniram_get_shared_processor_registration().should_distributor_server_stop()
        if x:
            self.__logger.notice('should_terminate now')
        return x

    def handle_incoming_connection(self, connection: socket.socket, address):
        """

        :param connection:
        :param address:
        :return:
        """

        # message types
        # 0. stop the server - done
        # 1. register a new processor - done
        # 2. unregister a new processor - done
        # 3. let a processor do some job
        #   3.1 and wait for its response
        #   3.2 or let it stop on halfway
        # 4. heartbeat i.e. PING PONG = done

        processor_name = None

        try:
            while True:
                try:
                    received = b''
                    base_message = BaseRequestMessage()
                    while True:
                        buffer = connection.recv(4096)
                        if len(buffer) <= 0:
                            raise ProcessorConnectionLost()
                        received += buffer
                        try:
                            base_message.load(received)
                            break
                        except json.decoder.JSONDecodeError:
                            # the json string is not end yet
                            pass

                    self.__logger.notice(f'handle_incoming_connection received {received}')
                    # now, the base_message is loaded

                    action = base_message.read_action()
                    request_message_for_action_class_name = 'RequestMessageAs' + action
                    request_message_for_action_class = CommonHelper.class_with_class_path(
                        'adoniram.message.request.' + request_message_for_action_class_name
                    )

                    self.__logger.info(
                        f'handle_client_conneciton request_message_for_action_class {request_message_for_action_class}')

                    if not issubclass(BaseRequestMessage.__class__, request_message_for_action_class.__class__):
                        raise BadMessageError('Unsupported Action', received)

                    request_message_for_action: BaseRequestMessage = request_message_for_action_class()
                    request_message_for_action.set_message_dict(base_message.get_message_dict())

                    try:
                        if processor_name is None:
                            processor_name = request_message_for_action.read_processor_name()
                        else:
                            if processor_name != request_message_for_action.read_processor_name():
                                raise BadMessageError(
                                    'processor_name is not same with registered',
                                    request_message_for_action.get_message_as_bytes()
                                )
                        request_message_for_action.handle(connection)
                        self.__logger.info("RESPONSE AS DONE")

                        if isinstance(request_message_for_action, RequestMessageAsShutdownServer):
                            self.__logger.critical('RequestMessageAsShutdownServer RECEIVED')
                            break

                    except HandleMessageError as e:
                        ResponseMessageAsRequestHandleError(e.__str__()).respond_to_client(connection)
                        self.__logger.error(f"RESPONSE AS HandleMessageError: {e}")
                except BadMessageError as e:
                    # notify client, ERROR
                    ResponseMessageAsRequestFormatError(e.__str__()).respond_to_client(connection)
                    self.__logger.error(f"RESPONSE AS BadMessageError: {e}")
        except ProcessorConnectionLost:
            self.__logger.critical('ProcessorConnectionLost', processor_name)

        self.__logger.notice('HERE THREAD ENDS', {'thread': threading.current_thread().name})
