'test comctl.Button and winuser.DrawIcon on form.ClientForm'

from pywingui.windows import *
from pywingui.wtl import *
from pywingui.lib import form

from pywingui import gdi
from pywingui import comctl
from pywingui import winuser

class MyForm(form.Form):
	_window_icon_ = Icon('blinky.ico')
	_window_icon_sm_ = _window_icon_
	_window_background_ = 0 #prevents windows from redrawing background, prevent flicker
	_window_class_style_ = CS_HREDRAW | CS_VREDRAW#make windows invalidate window on resize

	_window_title_ = __doc__

	def __init__(self, *args, **kwargs):
		self.ps = PAINTSTRUCT()

		#find some bitmap to show:
		try:
			self.bitmap = gdi.Bitmap('test.bmp')
		except:
			try:
				self.bitmap = gdi.Bitmap('c:\\Windows\\Web\\Wallpaper\\Bliss.bmp')
			except:
				print 'put a bitmap file "test.bmp" in the current directory'
				import os
				os._exit(-1)

		form.Form.__init__(self, *args, **kwargs)      

	def OnCreate(self, event):
		cf = form.ClientForm(parent = self)
		class button(comctl.Button):
			description = ''
			def OnClick(self, event):
				MessageBox(self.handle, self.description, 'Information', MB_ICONINFORMATION)
				event.handled = False
			msg_handler(WM_LBUTTONUP)(OnClick)
		button_bmp = button('...', parent = cf, orStyle = BS_BITMAP)
		button_bmp.SetImage(self.bitmap)
		button_bmp.description = 'Bitmap'
		cf.add((button_bmp, (5, 5, 64, 64)))
		button_ico = button(parent = cf, orStyle = BS_TEXT|BS_ICON)
		button_ico.SetImage(self._window_icon_, IMAGE_ICON)
		button_ico.description = 'Icon'
		cf.add((button_ico, (150, 5, 64, 64)))
		self.controls.Add(form.CTRL_VIEW, cf)
		self.client_form = cf

	def OnSize(self, event):
		form.Form.OnSize(self, event)
		winuser.DrawIcon(self.client_form.GetDC(), 150, 120, self._window_icon_.handle)
	msg_handler(WM_SIZE)(OnSize)

if __name__ == '__main__':
	mainForm = MyForm(rcPos = RECT(0, 0, 320, 240))        
	mainForm.ShowWindow()

	application = Application()
	application.Run()
