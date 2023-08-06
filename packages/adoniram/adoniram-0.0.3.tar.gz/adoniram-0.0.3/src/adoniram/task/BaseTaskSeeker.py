from abc import abstractmethod

from nehushtan.helper.CommonHelper import CommonHelper


class BaseTaskSeeker:
    def __init__(self, conditions: dict):
        self.__conditions = conditions

    def read_condition(self, key: tuple, default=None):
        return CommonHelper.read_dictionary(self.__conditions, key, default)

    @abstractmethod
    def seek_one_task_reference_for_processor(self):
        """
        Just seek a task, and return the reference;
        Or return None
        :return:
        """
        pass
