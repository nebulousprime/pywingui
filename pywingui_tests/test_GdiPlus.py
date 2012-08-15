'GdiPlus example based on pyWinGUI (Maxim Kolosov)'

from random import seed, randint

from pywingui import gdiplusflat as gdiplus
from pywingui import gdi
from pywingui.wtl import *
from pywingui.winuser import *
from pywingui.version_microsoft import WINVER

class main_window(Window):
	_window_title_ = __doc__
	_window_background_ = gdi.GetStockObject(gdi.LTGRAY_BRUSH)
	_window_icon_ = _window_icon_sm_ = Icon(lpIconName = IDI_ASTERISK)
	pt_size = 11# count points
	set_size = 3# count figures
	pt = (POINT*pt_size)((10, 10), (100, 10), (50, 100), (10, 10),# 0 figure (triangle)
		(10, 110), (200, 110), (200, 180), (10, 180), (10, 110),# 1 figure (parallelogram)
		(10, 200), (200, 200))# 2 figure (line)
	pts = (c_ulong*set_size)(4, 5, 2)# count points in every figure

	def OnDestroy(self, event):
		application.Quit()

	def OnPaint(self, event):
		ps = PAINTSTRUCT()
		ps.fErase = True
		hdc = self.BeginPaint(ps)
		rect = self.GetClientRect()
		self.Drawing_a_Shaded_Rectangle(hdc, rect)
		status, graphics = gdiplus.GdipCreateFromHDC(hdc)
		status, pen = gdiplus.GdipCreatePen1(gdiplus.MakeARGB(100, 0, 0, 255), 30.0)
		status = gdiplus.GdipDrawLineI(graphics, pen, 0, 0, rect.width, rect.height)
		status = gdiplus.GdipDrawLineI(graphics, pen, rect.width, 0, 0, rect.height)
		self.EndPaint(ps)

	msg_handler(WM_DESTROY)(OnDestroy)
	msg_handler(WM_PAINT)(OnPaint)

	def Drawing_a_Shaded_Rectangle(self, hdc, rc):
		vert = (gdi.TRIVERTEX*2)()
		gRect = gdi.GRADIENT_RECT()
		vert[0].x      = 0
		vert[0].y      = 0
		vert[0].Red    = randint(0x0000, 0xffff)#0xff00
		vert[0].Green  = randint(0x0000, 0xffff)#0xff00
		vert[0].Blue   = randint(0x0000, 0xffff)#0x0000
		vert[0].Alpha  = 0x8000
		vert[1].x      = rc.width
		vert[1].y      = rc.height
		vert[1].Red    = randint(0x0000, 0xffff)#0x0000
		vert[1].Green  = randint(0x0000, 0xffff)#0x0000
		vert[1].Blue   = randint(0x0000, 0xffff)#0xff00
		vert[1].Alpha  = 0x8000
		gRect.UpperLeft  = 0
		gRect.LowerRight = 1
		gdi.GradientFill(hdc, vert, 2, byref(gRect), 1, gdi.GRADIENT_FILL_RECT_H)

if __name__ == '__main__':
	# Initialize GDI+
	gdiplusToken = pointer(c_ulong())
	startup_input = gdiplus.GdiplusStartupInput(1, cast(None, gdiplus.DebugEventProc), False, False)
	gdiplus.GdiplusStartup(byref(gdiplusToken), startup_input, None)

	mw = main_window(rcPos = RECT(0, 0, 320, 240))
	application = Application()
	application.Run()

	# Shutdown GDI+
	gdiplus.GdiplusShutdown(gdiplusToken)
