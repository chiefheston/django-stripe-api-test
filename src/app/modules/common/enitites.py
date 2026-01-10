from dataclasses import dataclass, field


@dataclass
class Entity:
    id: int | None = field(
        default=None,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: "Entity") -> bool:
        return self.id == __value.id
