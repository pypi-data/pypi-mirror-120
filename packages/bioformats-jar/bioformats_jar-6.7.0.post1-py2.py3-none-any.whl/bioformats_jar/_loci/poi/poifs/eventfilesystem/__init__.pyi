import java.lang
import bioformats_jar._loci.common
import bioformats_jar._loci.poi.poifs.filesystem
import typing



class POIFSReader:
    def __init__(self): ...
    @staticmethod
    def main(stringArray: typing.List[java.lang.String]) -> None: ...
    def read(self, randomAccessInputStream: bioformats_jar._loci.common.RandomAccessInputStream, int: int) -> None: ...
    @typing.overload
    def registerListener(self, pOIFSReaderListener: 'POIFSReaderListener') -> None: ...
    @typing.overload
    def registerListener(self, pOIFSReaderListener: 'POIFSReaderListener', string: typing.Union[java.lang.String, str]) -> None: ...
    @typing.overload
    def registerListener(self, pOIFSReaderListener: 'POIFSReaderListener', pOIFSDocumentPath: bioformats_jar._loci.poi.poifs.filesystem.POIFSDocumentPath, string: typing.Union[java.lang.String, str]) -> None: ...

class POIFSReaderEvent:
    def getName(self) -> java.lang.String: ...
    def getPath(self) -> bioformats_jar._loci.poi.poifs.filesystem.POIFSDocumentPath: ...
    def getStream(self) -> bioformats_jar._loci.poi.poifs.filesystem.DocumentInputStream: ...

class POIFSReaderListener:
    def processPOIFSReaderEvent(self, pOIFSReaderEvent: POIFSReaderEvent) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.poi.poifs.eventfilesystem")``.

    POIFSReader: typing.Type[POIFSReader]
    POIFSReaderEvent: typing.Type[POIFSReaderEvent]
    POIFSReaderListener: typing.Type[POIFSReaderListener]
