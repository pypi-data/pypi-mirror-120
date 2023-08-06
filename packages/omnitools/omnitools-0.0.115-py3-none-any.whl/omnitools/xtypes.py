from typing import *


__ALL__ = ["str_or_bytes", "list_or_dict", "list_or_tuple", "bytes_or_list", "key_pair_format", "color_value", "encryptedsocket_function", "Obj", "HeadersDict"]


str_or_bytes = Union[str, bytes]
list_or_dict = Union[list, dict]
list_or_tuple = Union[list, tuple]
bytes_or_list = Union[bytes, list]
key_pair_format = Dict[str, bytes]
color_value = Tuple[int, int, int]
encryptedsocket_function = Dict[str, Callable[[Any], Any]]


class Obj(object):
    def __init__(self, d: dict=None):
        if d is not None:
            if isinstance(d, dict):
                self.__dict__.update(d)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class HeadersDict(Obj):
    def __init__(self, d: dict=None):
        if d is not None:
            if isinstance(d, dict):
                for k in d:
                    self.__setitem__(k, d[k])
        super().__init__()

    def __getitem__(self, key):
        return self.__dict__[self.rkey(key)]

    def __setitem__(self, key, value):
        self.__dict__[self.rkey(key)] = value

    def __delitem__(self, key):
        del self.__dict__[self.rkey(key)]

    def __contains__(self, key):
        return self.rkey(key) in self.__dict__

    @staticmethod
    def rkey(key):
        return "-".join(_[0].upper()+_[1:] for _ in key.lower().replace(" ", "-").replace("_", "-").split("-"))


