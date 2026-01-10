from dataclasses import dataclass


@dataclass(eq=False)
class DomainException(Exception):
    message: str


@dataclass(eq=False)
class DomainTypeException(Exception):
    message: str


@dataclass(eq=False)
class ApplicationException(Exception):
    message: str
