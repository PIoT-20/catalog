class ConnectionInfo:
    def __init__(self, protocol: str, emulator: str, start_time: str, end_time: str, frequency_seconds: int) -> None:
        self.protocol: str = protocol
        self.emulator_type: str = emulator
        self.start_time: str= start_time
        self.end_time: str= end_time
        self.frequency_seconds: int= frequency_seconds


