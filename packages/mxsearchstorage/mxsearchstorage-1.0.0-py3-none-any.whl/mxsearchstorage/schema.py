from enum import Enum


class BatchError(Exception):
    def __init__(self, message):
        self.message = message


class Type(Enum):
    PRIMARY=1
    SECONDARY=2