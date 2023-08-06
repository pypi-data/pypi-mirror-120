import ij
import bioformats_jar._loci.plugins
import typing



class Exporter:
    def __init__(self, lociExporter: bioformats_jar._loci.plugins.LociExporter, imagePlus: ij.ImagePlus): ...
    def run(self) -> None: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.plugins.out")``.

    Exporter: typing.Type[Exporter]
