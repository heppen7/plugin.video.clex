import xbmcgui
import xbmc

from .common import Common

com = Common()

class Dialogs:
    def __init__(self) -> None:
        pass
    
    def pin_code(self, code):
        heading = com.lang(32001)
        message = com.lang(32002).format(code)
        return xbmcgui.Dialog().yesno(heading, message, com.lang(32004), com.lang(32003), 9000*1000)
