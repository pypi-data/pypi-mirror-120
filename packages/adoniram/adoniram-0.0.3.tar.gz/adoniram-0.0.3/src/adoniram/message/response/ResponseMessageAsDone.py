from adoniram.message.BaseResponseMessage import BaseResponseMessage


class ResponseMessageAsDone(BaseResponseMessage):
    CODE = 'Done'

    def __init__(self, data=None):
        super().__init__(self.CODE, data)
