from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger

from adoniram.distributor.ProcessorRegistration import ProcessorRegistration

shared_processor_registration: ProcessorRegistration
adoniram_config: dict


def adoniram_load_config(config_dict: dict):
    global adoniram_config
    adoniram_config = config_dict


def adoniram_read_config(keychain: tuple, default=None):
    global adoniram_config
    return CommonHelper.read_dictionary(adoniram_config, keychain, default)


def adoniram_make_server_logger(title: str):
    return NehushtanFileLogger(title, adoniram_read_config(('server', 'logger', 'dir')))


def adoniram_distributor_init_shared_kit():
    global shared_processor_registration
    shared_processor_registration = ProcessorRegistration()


def adoniram_get_shared_processor_registration():
    global shared_processor_registration
    # print(threading.current_thread().getName(),shared_processor_registration,shared_processor_registration.should_distributor_server_stop())
    return shared_processor_registration
