import json

from nehushtan.helper.CommonHelper import CommonHelper

from adoniram.exception.BadMessageError import BadMessageError


class BaseMessage:
    def __init__(self, raw: bytes = None):
        self.__message_dict = {}
        self.__raw = raw
        if raw:
            self.load(raw)

    def load(self, raw: bytes):
        """
        would raise `json.decoder.JSONDecodeError` when raw is not a complete json;
        would raise `BadMessageError` when json is not a dict or other format error.
        :param raw:
        :return:
        """
        self.__raw = raw
        decoded: dict = json.loads(raw.decode())
        if type(decoded) is not dict:
            raise BadMessageError('Message is not a dict', raw)
        self.__message_dict = decoded
        return self

    def get_message_dict(self):
        return self.__message_dict

    def read(self, keychain: tuple, default: any = None):
        return CommonHelper.read_dictionary(self.__message_dict, keychain, default)

    def set_message_dict(self, m: dict):
        self.__message_dict = m
        self.__raw = json.dumps(m).encode()
        return self

    def get_message_as_bytes(self):
        return self.__raw
