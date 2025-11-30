from dataclasses import dataclass

@dataclass(slots=True)
class Clock:
    name: str
    doi: str