from nehushtan.helper.CommonHelper import CommonHelper

from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone
from adoniram.message.response.ResponseMessageAsRequestHandleError import ResponseMessageAsRequestHandleError
from adoniram.task.BaseTaskHandler import BaseTaskHandler


class RequestMessageAsHandleTask(BaseRequestMessage):
    """
    This is a mistake design
    """

    def defined_request_action(self) -> str:
        return 'HandleTask'

    def handle_request_for_response(self) -> BaseResponseMessage:
        # get the full path for task handler class (with namespace)
        task_handler_class_path = self.read(('task_handler_class',))
        task_reference = self.read(('task_reference',))

        if not task_reference:
            return ResponseMessageAsRequestHandleError('TASK REFERENCE NOT VALID')

        task_handler_class = CommonHelper.class_with_class_path(task_handler_class_path)
        if not issubclass(task_handler_class, BaseTaskHandler):
            return ResponseMessageAsRequestHandleError('TASK HANDLER CLASS NOT VALID')

        try:
            task_handler = task_handler_class(task_reference)
            task_handler.handle()

            return ResponseMessageAsDone(
                {
                    'task_reference': task_handler.get_task_reference(),
                    'result': task_handler.get_task_handle_result(),
                    'feedback': task_handler.get_task_handle_feedback(),
                }
            )

        except Exception as e:
            return ResponseMessageAsRequestHandleError(f'TASK HANDLER REPORTS ERROR: {e}')
