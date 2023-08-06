class ProcessorNameConflictError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Processor with name [{name}] is already registered')
