from dataclasses import dataclass

@dataclass(slots=True)
class Condition:
    name: str
    duration: str