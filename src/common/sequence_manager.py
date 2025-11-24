from typing import Dict


class SequenceCounter:
    name = 0
    sequence = 0

    def __init__(self, name: str):
        self.name = name
        self.sequence = 0

    @classmethod
    def get_sequence(cls) -> int:
        current_sequence = cls.sequence
        cls.sequence += 1
        return current_sequence

class SequenceManager:

    sequence_dict: Dict[str, SequenceCounter] = {}

    @classmethod
    def get_sequence_instance(cls, key):
        if key not in cls.sequence_dict:
            cls.sequence_dict[key] = SequenceCounter(key)
        return cls.sequence_dict[key]

    @classmethod
    def remove_sequence_instance(cls, key):
        if key not in cls.sequence_dict:
            return
        cls.sequence_dict.pop(key)

    @classmethod
    def get_name_by_instance(cls, sequence_counter: SequenceCounter):
        return sequence_counter.name

    @classmethod
    def get_name_by_key(cls, key: str):
        if key not in cls.sequence_dict:
            return None
        return cls.sequence_dict[key].name