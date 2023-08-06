import java.lang
import java.util
import typing



class POIFSViewEngine:
    def __init__(self): ...
    @staticmethod
    def inspectViewable(object: typing.Any, boolean: bool, int: int, string: typing.Union[java.lang.String, str]) -> java.util.List: ...

class POIFSViewable:
    def getShortDescription(self) -> java.lang.String: ...
    def getViewableArray(self) -> typing.List[typing.Any]: ...
    def getViewableIterator(self) -> java.util.Iterator: ...
    def preferArray(self) -> bool: ...

class POIFSViewer:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.List[java.lang.String]) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.poi.poifs.dev")``.

    POIFSViewEngine: typing.Type[POIFSViewEngine]
    POIFSViewable: typing.Type[POIFSViewable]
    POIFSViewer: typing.Type[POIFSViewer]
