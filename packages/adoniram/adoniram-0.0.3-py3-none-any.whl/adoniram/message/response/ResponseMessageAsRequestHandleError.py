from adoniram.message.BaseResponseMessage import BaseResponseMessage


class ResponseMessageAsRequestHandleError(BaseResponseMessage):
    CODE = 'RequestHandleError'

    def __init__(self, data=None):
        super().__init__(self.CODE, data)
