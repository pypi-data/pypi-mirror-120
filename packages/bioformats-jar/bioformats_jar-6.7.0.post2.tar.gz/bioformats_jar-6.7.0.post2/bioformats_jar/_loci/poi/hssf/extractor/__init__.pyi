import java.lang
import bioformats_jar._loci.poi
import bioformats_jar._loci.poi.hssf.usermodel
import bioformats_jar._loci.poi.poifs.filesystem
import typing



class ExcelExtractor(loci.poi.POITextExtractor):
    @typing.overload
    def __init__(self, hSSFWorkbook: bioformats_jar._loci.poi.hssf.usermodel.HSSFWorkbook): ...
    @typing.overload
    def __init__(self, pOIFSFileSystem: bioformats_jar._loci.poi.poifs.filesystem.POIFSFileSystem): ...
    def getText(self) -> java.lang.String: ...
    def setFormulasNotResults(self, boolean: bool) -> None: ...
    def setIncludeSheetNames(self, boolean: bool) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.poi.hssf.extractor")``.

    ExcelExtractor: typing.Type[ExcelExtractor]
