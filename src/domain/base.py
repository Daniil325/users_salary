from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Entity:
    id: str = field(default_factory=uuid4, kw_only=True)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.__class__ == other.__class__ and self.id == other.id