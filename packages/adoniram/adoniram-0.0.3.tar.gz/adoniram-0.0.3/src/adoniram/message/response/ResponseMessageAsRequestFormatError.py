from adoniram.message.BaseResponseMessage import BaseResponseMessage


class ResponseMessageAsRequestFormatError(BaseResponseMessage):
    CODE = 'RequestFormatError'

    def __init__(self, data=None):
        super().__init__(self.CODE, data)
