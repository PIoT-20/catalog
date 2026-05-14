class ConnectionInfoModel:
    def __init__(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("Connection info data must be a dictionary")
        if "protocol" not in data or not data["protocol"]:
            raise ValueError("Connection info must contain a 'protocol' field")
        self.data = data

    @classmethod
    def from_dict(cls, d):
        if not d:
            raise ValueError("Connection info cannot be None or empty")
        return cls(d)

    def to_dict(self) -> dict:
        return self.data
