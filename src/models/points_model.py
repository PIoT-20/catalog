class PointModel:
    def __init__(self,  path_id: str='', level=0) -> None:
        self.path_id = path_id
        self.level: int =level

    @classmethod
    def from_dict(cls, d):
        return cls(
            path_id=d.get("path_id"),
            level=d.get("level")
        )

    def to_create_dict(self) -> dict:
        return {
            "path_id": self.path_id,
            "level": self.level
        }
