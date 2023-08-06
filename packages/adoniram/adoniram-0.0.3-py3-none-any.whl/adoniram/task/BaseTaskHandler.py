from abc import abstractmethod


class BaseTaskHandler:
    def __init__(self, task_reference):
        self.__task_reference = task_reference

        self.__task_handle_result: bool = False  # True or False in my opinion
        self.__task_handle_feedback: str = ''

        self._load_task_detail()

    def get_task_reference(self):
        return self.__task_reference

    def set_task_reference(self, task_reference):
        self.__task_reference = task_reference

    def get_task_handle_result(self):
        return self.__task_handle_result

    def set_task_handle_result(self, task_handle_result):
        self.__task_handle_result = task_handle_result

    def get_task_handle_feedback(self):
        return self.__task_handle_feedback

    def set_task_handle_feedback(self, task_handle_feedback: str):
        self.__task_handle_feedback = task_handle_feedback

    @abstractmethod
    def _load_task_detail(self):
        pass

    @abstractmethod
    def handle(self):
        """
        Must set the result and feedback
        :return:
        """
        pass
