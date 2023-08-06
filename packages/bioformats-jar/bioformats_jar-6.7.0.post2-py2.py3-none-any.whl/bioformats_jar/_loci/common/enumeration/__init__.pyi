import java.lang
import typing



class CodedEnum:
    def getCode(self) -> int: ...

class EnumException(java.lang.RuntimeException):
    @typing.overload
    def __init__(self): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str]): ...
    @typing.overload
    def __init__(self, string: typing.Union[java.lang.String, str], throwable: java.lang.Throwable): ...
    @typing.overload
    def __init__(self, throwable: java.lang.Throwable): ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.common.enumeration")``.

    CodedEnum: typing.Type[CodedEnum]
    EnumException: typing.Type[EnumException]
