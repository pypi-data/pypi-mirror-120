import bioformats_jar._loci.common
import bioformats_jar._loci.formats
import bioformats_jar._loci.plugins
import bioformats_jar._loci.poi
import typing


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci")``.

    common: bioformats_jar._loci.common.__module_protocol__
    formats: bioformats_jar._loci.formats.__module_protocol__
    plugins: bioformats_jar._loci.plugins.__module_protocol__
    poi: bioformats_jar._loci.poi.__module_protocol__
