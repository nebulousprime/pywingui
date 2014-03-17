'FileMapping Example'

str_parent_environment = ''
str_environment = repr(globals())
BUF_SIZE = len(str_environment) or 1024

import sys
if sys.hexversion >= 0x03000000:
	type_str = bytes
	type_unicode = str
else:
	type_str = str
	type_unicode = unicode

from subprocess import Popen

from pywingui.windows import *
from pywingui.wtl import *
from pywingui import comctl
from pywingui.lib import form
from pywingui.winuser import FindWindow

comctl.InitCommonControls(comctl.ICC_USEREX_CLASSES)

class button(comctl.Button):
	pBuf = None
	hMapFile = None
	child_process = None
	def __del__(self):
		self.check()
	def check(self):
		if self.pBuf:
			UnmapViewOfFile(self.pBuf)
			self.pBuf = None
		if self.hMapFile:
			CloseHandle(self.hMapFile)
			self.hMapFile = None
		if self.child_process:
			if self.child_process.poll() is None:
				self.child_process.terminate()
	def OnClick(self, event):
		self.check()
		self.hMapFile = CreateFileMapping(INVALID_HANDLE_VALUE, SECURITY_ATTRIBUTES(), PAGE_READWRITE, 0, BUF_SIZE, 'parent_environment_data')
		if self.hMapFile:
			self.pBuf = MapViewOfFile(self.hMapFile, FILE_MAP_ALL_ACCESS, 0, 0, BUF_SIZE)
			if self.pBuf:
				c_str = create_string_buffer(str_environment)
				memmove(self.pBuf, c_str, BUF_SIZE)
				command = '%s test_FileMapping.py -child_process' % sys.executable
				self.child_process = Popen(command)
			else:
				CloseHandle(self.hMapFile)
		event.handled = False
	msg_handler(WM_LBUTTONUP)(OnClick)

class Form(form.Form):
	_form_menu_ = [(MF_POPUP, "&File", [(MF_STRING, "&Exit", form.ID_EXIT)])]

	def __init__(self):
		x = 0
		if str_parent_environment:
			x = 320
		form.Form.__init__(self, rcPos = RECT(x, 0, x+320, 240))

	def OnCreate(self, event):
		if str_parent_environment:
			st = comctl.StaticText(str_parent_environment, parent = self)
			self.controls.Add(form.CTRL_VIEW, st)
		else:
			cf = form.ClientForm(parent = self)
			btn = button('new process window', parent = cf, orStyle = BS_TEXT)
			cf.add((btn, (5, 5, 200, 25)))
			self.controls.Add(form.CTRL_VIEW, cf)
		self.controls.Add(form.CTRL_STATUSBAR, comctl.StatusBar(parent = self))

if __name__ == '__main__':
	if '-child_process' in sys.argv:
		hMapFile = OpenFileMapping(FILE_MAP_ALL_ACCESS, False, 'parent_environment_data')
		if hMapFile:
			pBuf = MapViewOfFile(hMapFile, FILE_MAP_ALL_ACCESS, 0, 0, BUF_SIZE)
			if pBuf:
				str_parent_environment = string_at(pBuf)
				UnmapViewOfFile(pBuf)
			CloseHandle(hMapFile)

	mainForm = Form()
	if str_parent_environment:
		mainForm.SetText(__doc__ + ' (child window)')
	else:
		mainForm.SetText(__doc__ + ' (parent window)')
	mainForm.ShowWindow()

	application = Application()
	application.Run()

	if not str_parent_environment:
		hwnd = FindWindow(0, type_unicode(__doc__ + ' (child window)'))
		if not UNICODE and not hwnd:
			hwnd = FindWindow(0, type_str(__doc__ + ' (child window)'))
		if hwnd:
			SendMessage(hwnd, WM_CLOSE, 0, 0)
