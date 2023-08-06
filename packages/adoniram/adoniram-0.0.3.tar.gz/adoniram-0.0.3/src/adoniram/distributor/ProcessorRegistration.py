from threading import Lock

from adoniram.exception.ProcessorNameConflictError import ProcessorNameConflictError
from adoniram.exception.ProcessorNotRegisteredError import ProcessorNotRegisteredError
from adoniram.exception.ProcessorRegistrationLocked import ProcessorRegistrationLocked


class ProcessorRegistration:
    def __init__(self):
        self.__processor_dict = {}
        self.__lock = Lock()
        self.__distributor_server_should_stop = False

    def stop_distributor_server(self):
        if self.__lock.acquire(blocking=True, timeout=5):
            self.__distributor_server_should_stop = True
            self.__lock.release()
        else:
            raise ProcessorRegistrationLocked()

    def should_distributor_server_stop(self):
        return self.__distributor_server_should_stop

    def register(self, name: str, host, port):
        if self.__lock.acquire(blocking=True, timeout=5):
            try:
                _ = self.__processor_dict[name]
                raise ProcessorNameConflictError(name)
            except KeyError:
                self.__processor_dict[name] = {
                    'host': host,
                    'port': port,
                    'processing_tasks': {},
                }

            self.__lock.release()
        else:
            raise ProcessorRegistrationLocked()

    def unregister(self, name: str):
        if self.__lock.acquire(blocking=True, timeout=5):
            try:
                x = self.__processor_dict[name]

                if len(x['processing_tasks']):
                    # todo let the `processing_task`s dead
                    pass

                del self.__processor_dict[name]
            except KeyError:
                raise ProcessorNotRegisteredError(name)

            self.__lock.release()
        else:
            raise ProcessorRegistrationLocked()
