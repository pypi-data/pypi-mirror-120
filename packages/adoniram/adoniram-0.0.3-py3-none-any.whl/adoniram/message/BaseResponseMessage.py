import socket

from adoniram.exception.BadMessageError import BadMessageError
from adoniram.message.BaseMessage import BaseMessage


class BaseResponseMessage(BaseMessage):
    """
    FORMAT {"code":"OK","data":...}
    """

    def __init__(self, code: str, data=None):
        super().__init__()

        self.set_message_dict({'code': code, 'data': data})

    def read_code(self):
        x = self.read(('code',))
        if not x:
            raise BadMessageError('Message with Empty Code', self.__raw)
        return x

    def read_data(self, keychain: tuple, default: any = None):
        return self.read(('data',) + keychain, default)

    def respond_to_client(self, connection: socket.socket):
        b = self.get_message_as_bytes()
        sent_bytes = connection.send(b)
        # do you need check sent length and expected length?
        return self
