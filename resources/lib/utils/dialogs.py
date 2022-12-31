import xbmcgui
import xbmc

from .config import lang

class Dialogs:
    def __init__(self) -> None:
        pass
    
    def pin_code(self, code):
        heading = lang(32001)
        message = lang(32002).format(code)
        return xbmcgui.Dialog().yesno(heading, message, lang(32004), lang(32003), 9000*1000)

    def notification(self, head, message):
        xbmcgui.Dialog().notification(head, message)