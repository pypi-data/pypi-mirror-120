import java.lang
import bioformats_jar._loci.poi.ddf
import bioformats_jar._loci.poi.dev
import bioformats_jar._loci.poi.hpsf
import bioformats_jar._loci.poi.hssf
import bioformats_jar._loci.poi.poifs
import bioformats_jar._loci.poi.util
import typing



class POIDocument:
    def __init__(self): ...
    def getDocumentSummaryInformation(self) -> bioformats_jar._loci.poi.hpsf.DocumentSummaryInformation: ...
    def getSummaryInformation(self) -> bioformats_jar._loci.poi.hpsf.SummaryInformation: ...

class POITextExtractor:
    def __init__(self, pOIDocument: POIDocument): ...
    def getText(self) -> java.lang.String: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.poi")``.

    POIDocument: typing.Type[POIDocument]
    POITextExtractor: typing.Type[POITextExtractor]
    ddf: bioformats_jar._loci.poi.ddf.__module_protocol__
    dev: bioformats_jar._loci.poi.dev.__module_protocol__
    hpsf: bioformats_jar._loci.poi.hpsf.__module_protocol__
    hssf: bioformats_jar._loci.poi.hssf.__module_protocol__
    poifs: bioformats_jar._loci.poi.poifs.__module_protocol__
    util: bioformats_jar._loci.poi.util.__module_protocol__
