from pywingui.windows import *
from pywingui.wtl import *
from pywingui import comctl

class TrackBar(comctl.TrackBar):

    def __init__(self, *args, **kwargs):
        comctl.TrackBar.__init__(self, *args, **kwargs)
        self.InterceptParent(nMsg = [WM_HSCROLL, WM_VSCROLL])

    def OnScroll(self, event):
        pass

    _msg_map_ = MSG_MAP([MSG_HANDLER(WM_HSCROLL, OnScroll),
                         MSG_HANDLER(WM_VSCROLL, OnScroll)])
