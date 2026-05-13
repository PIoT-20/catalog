class SensorModel:
    def __init__(self, type: str, model: str, unit: str) -> None:
        self.type = type
        self.model = model
        self.unit = unit

    @classmethod
    def from_dict(cls, d):
        return cls(type=d.get("type"), model=d.get("model"), unit=d.get("unit"))

    def to_dict(self) -> dict:
        return {"type": self.type, "model": self.model, "unit": self.unit}
