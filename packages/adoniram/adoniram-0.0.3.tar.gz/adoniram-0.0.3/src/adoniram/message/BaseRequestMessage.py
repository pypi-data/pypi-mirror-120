import socket
from abc import abstractmethod
from typing import final

from adoniram.exception.BadMessageError import BadMessageError
from adoniram.exception.HandleMessageError import HandleMessageError
from adoniram.message.BaseMessage import BaseMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage


class BaseRequestMessage(BaseMessage):
    """
    FORMAT {"action":"XXX","processor_name":"YYY",...}
    """

    @abstractmethod
    def defined_request_action(self) -> str:
        """
        FOR CLIENt
        :return:
        """
        pass

    def build(self, processor_name: str, **kwargs):
        """
        FOR CLIENT
        :param processor_name:
        :param kwargs:
        :return:
        """
        x = {
            'action': self.defined_request_action(),
            'processor_name': processor_name,
        }

        for k, v in kwargs.items():
            x[k] = v

        self.set_message_dict(x)
        return self

    def read_action(self):
        x = self.read(('action',))
        if not x:
            raise BadMessageError('Message with Empty Action', self.get_message_as_bytes())
        return x

    def read_processor_name(self):
        x = self.read(('processor_name',))
        if not x:
            raise BadMessageError('Message with Empty Processor Name', self.get_message_as_bytes())
        return x

    @abstractmethod
    def handle_request_for_response(self) -> BaseResponseMessage:
        """
        FOR SERVER
        to be overrode
        :return:
        """
        raise NotImplementedError()

    @final
    def handle(self, connection: socket.socket):
        """
        FOR SERVER
        :param connection:
        :return:
        """
        try:
            response = self.handle_request_for_response()
            response.respond_to_client(connection)
        except Exception as e:
            raise HandleMessageError(e.__str__()) from e
