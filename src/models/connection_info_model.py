class ConnectionInfoModel:
    def __init__(
        self,
        protocol: str,
        emulator: str,
        start_time: str,
        end_time: str,
        frequency_seconds: int,
    ) -> None:
        self.protocol: str = protocol
        self.emulator_type: str = emulator
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.frequency_seconds: int = frequency_seconds

    @classmethod
    def from_dict(cls, d):
        return cls(
            protocol=d.get("protocol"),
            emulator=d.get("emulator"),
            start_time=d.get("start_time"),
            end_time=d.get("end_time"),
            frequency_seconds=d.get("frequency_seconds"),
        )

    def to_dict(self):
        return {
            "protocol": self.protocol,
            "emulator": self.emulator_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "frequency_seconds": self.frequency_seconds,
        }
