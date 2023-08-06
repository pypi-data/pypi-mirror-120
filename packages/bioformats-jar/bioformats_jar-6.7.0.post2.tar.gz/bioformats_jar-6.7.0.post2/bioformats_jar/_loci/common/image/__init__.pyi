import typing



class IImageScaler:
    def downsample(self, byteArray: typing.List[int], int: int, int2: int, double: float, int3: int, boolean: bool, boolean2: bool, int4: int, boolean3: bool) -> typing.List[int]: ...

class SimpleImageScaler(IImageScaler):
    def __init__(self): ...
    def downsample(self, byteArray: typing.List[int], int: int, int2: int, double: float, int3: int, boolean: bool, boolean2: bool, int4: int, boolean3: bool) -> typing.List[int]: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.common.image")``.

    IImageScaler: typing.Type[IImageScaler]
    SimpleImageScaler: typing.Type[SimpleImageScaler]
