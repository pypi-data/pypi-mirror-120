import ij.plugin
import java.awt.datatransfer
import java.awt.event
import java.lang
import javax.swing
import typing



class ShortcutPanel(javax.swing.JPanel, java.awt.event.ActionListener, ij.plugin.PlugIn):
    def __init__(self): ...
    def actionPerformed(self, actionEvent: java.awt.event.ActionEvent) -> None: ...
    def open(self, string: typing.Union[java.lang.String, str]) -> None: ...
    def run(self, string: typing.Union[java.lang.String, str]) -> None: ...
    @staticmethod
    def runPlugIn(string: typing.Union[java.lang.String, str], string2: typing.Union[java.lang.String, str]) -> None: ...

class ShortcutTransferHandler(javax.swing.TransferHandler):
    def __init__(self, shortcutPanel: ShortcutPanel): ...
    @typing.overload
    def canImport(self, transferSupport: javax.swing.TransferHandler.TransferSupport) -> bool: ...
    @typing.overload
    def canImport(self, jComponent: javax.swing.JComponent, dataFlavorArray: typing.List[java.awt.datatransfer.DataFlavor]) -> bool: ...
    @typing.overload
    def importData(self, transferSupport: javax.swing.TransferHandler.TransferSupport) -> bool: ...
    @typing.overload
    def importData(self, jComponent: javax.swing.JComponent, transferable: java.awt.datatransfer.Transferable) -> bool: ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("loci.plugins.shortcut")``.

    ShortcutPanel: typing.Type[ShortcutPanel]
    ShortcutTransferHandler: typing.Type[ShortcutTransferHandler]
