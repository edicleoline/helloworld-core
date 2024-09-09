from ulid import ULID
from dataclasses import dataclass, asdict
from inspect import getmembers

@dataclass
class BaseEntity:
    id: ULID = ''

    @classmethod
    def from_dict(cls, d = None):
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    def describe(self):
        atts = getmembers(self)

        attributes = list()
        for att in atts:
            c0 = not att[0].startswith('__')
            c1 = not callable(att[1])

            if c0 and c1:
                attr_name = att[0]
                attr_type = type(att[1]).__name__
                if attr_type == 'ULID': attr_type = 'str'

                attribute = (attr_name, attr_type)
                attributes.append(attribute)

        return attributes