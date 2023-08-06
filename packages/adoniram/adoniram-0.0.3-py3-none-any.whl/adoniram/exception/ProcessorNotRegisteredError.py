class ProcessorNotRegisteredError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Processor with name [{name}] is not registered')
