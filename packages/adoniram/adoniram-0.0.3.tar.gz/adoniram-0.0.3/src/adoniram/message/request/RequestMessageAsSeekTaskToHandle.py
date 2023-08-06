from nehushtan.helper.CommonHelper import CommonHelper

from adoniram.message.BaseRequestMessage import BaseRequestMessage
from adoniram.message.BaseResponseMessage import BaseResponseMessage
from adoniram.message.response.ResponseMessageAsDone import ResponseMessageAsDone
from adoniram.message.response.ResponseMessageAsRequestHandleError import ResponseMessageAsRequestHandleError
from adoniram.task.BaseTaskSeeker import BaseTaskSeeker


class RequestMessageAsSeekTaskToHandle(BaseRequestMessage):
    def defined_request_action(self) -> str:
        return 'SeekTaskToHandle'

    def handle_request_for_response(self) -> BaseResponseMessage:
        # get the full path for task handler class (with namespace)
        task_seeker_class_path = self.read(('task_seeker_class',))

        task_seek_conditions = self.read(('task_seek_conditions',), {})

        task_seeker_class = CommonHelper.class_with_class_path(task_seeker_class_path)
        if not issubclass(task_seeker_class, BaseTaskSeeker):
            return ResponseMessageAsRequestHandleError('TASK HANDLER CLASS NOT VALID')

        try:
            task_reference = task_seeker_class(task_seek_conditions).seek_one_task_reference_for_processor()
            return ResponseMessageAsDone({'task_reference': task_reference})
        except Exception as e:
            return ResponseMessageAsRequestHandleError(f'TASK HANDLER REPORTS ERROR: {e}')
