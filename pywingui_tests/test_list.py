## 	   Copyright (c) 2003 Henk Punt

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the
## "Software"), to deal in the Software without restriction, including
## without limitation the rights to use, copy, modify, merge, publish,
## distribute, sublicense, and/or sell copies of the Software, and to
## permit persons to whom the Software is furnished to do so, subject to
## the following conditions:

## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
## OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

from pywingui.windows import *
from pywingui.wtl import *
from pywingui.comctl import *
from pywingui.lib import list
from pywingui.lib import form

blinkyIcon = Icon('blinky.ico')

columnDefs = [('column 0', 100), ('column 1', 150)]

InitCommonControls(ICC_LISTVIEW_CLASSES)

class MyList(list.List):
	_window_style_ = WS_CHILD | WS_VISIBLE | LVS_REPORT | LVS_EDITLABELS | LVS_SINGLESEL
	#~ _listview_style_ex_ = LVS_EX_FLATSB

	def OnPaint(self, event):
		#print "lpaint", self.handle
		width = self.clientRect.width
		for i in range(len(columnDefs) - 1):
			#self.SetColumnWidth(i, width / len(columnDefs))
			self.SetColumnWidth(i, -2)
		self.SetColumnWidth(len(columnDefs) - 1, -2)
		event.handled = False
	#~ msg_handler(WM_PAINT)(OnPaint)

	def OnWindowPosChanging(self, event):
		event.handled = False
	msg_handler(WM_WINDOWPOSCHANGED)(OnWindowPosChanging)

	def OnSize(self, event):
		#width = self.clientRect.width
		#~ ShowScrollBar(self.handle, SB_HORZ, False)
		self.SetRedraw(0)
		for i in range(len(columnDefs) - 1):
			#self.SetColumnWidth(i, width / len(columnDefs))
			self.SetColumnWidth(i, -2)
		self.SetColumnWidth(len(columnDefs) - 1, -2)
		self.SetRedraw(1)
		event.handled = False
	#~ msg_handler(WM_SIZE)(OnSize)

	#~ def OnLButtonDoubleClick(self, event):
		#~ print('OnLbuttonDoubleClick %d' % self.GetSelectedFocusedItem())
		#~ self.EditLabel(self.GetSelectedFocusedItem())
	#~ msg_handler(WM_LBUTTONDBLCLK)(OnLButtonDoubleClick)

	def OnDoubleClick(self, event):
		#~ pinfo = self.HitTest()
		#~ if pinfo:
			#~ print pinfo.pt, pinfo.flags, pinfo.iItem, pinfo.iSubItem
		#~ else:
			#~ print 'Error HitTest'
		nmlv = NMLISTVIEW.from_address(event.lParam)
		print('item %d, subitem %d, POINT(%d, %d)' % (nmlv.iItem, nmlv.iSubItem, nmlv.ptAction.x, nmlv.ptAction.y))
		if nmlv.iSubItem:
			hEdit = Edit(parent = self, style = WS_VISIBLE | WS_CHILD | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, orStyle = WS_EX_CLIENTEDGE | ES_AUTOHSCROLL)
			#~ hEdit.SetRectNp(rect)
			hEdit.SetText(self.GetItemText(nmlv.iItem, nmlv.iSubItem))
			hEdit.ShowWindow(SW_SHOWNORMAL)
		else:
			hEdit = self.EditLabel(nmlv.iItem)
	ntf_handler(NM_DBLCLK)(OnDoubleClick)

	def OnColumnClick(self, event):
		nmlv = NMLISTVIEW.from_address(int(event.lParam))
		print('column clicked! %d' % nmlv.iSubItem)
	ntf_handler(LVN_COLUMNCLICK)(OnColumnClick)

	def OnBeginLabelEdit(self, event):
		print('OnBeginLabelEdit %d' % self.GetSelectedFocusedItem())
		#~ hEdit = self.GetEditControl()
		#~ nmldi = NMLVDISPINFO.from_address(int(event.lParam))
		#~ print('Edit item %d' % nmldi.item[0].iItem)
		#~ return False
		return True
	#~ ntf_handler(LVN_BEGINLABELEDIT)(OnBeginLabelEdit)

	def OnEndLabelEdit(self, event):
		print('OnEndLabelEdit %d' % self.GetSelectedFocusedItem())
		text_size = 1024
		if UNICODE:
			text = type_unicode('\0') * text_size
		else:
			text = type_str('\0') * text_size
		hEdit = self.GetEditControl()
		GetWindowText(hEdit, text, text_size)
		#~ nmldi = NMLVDISPINFO.from_address(int(event.lParam))
		#~ print('Edit item %d' % nmldi.item[0].iItem)
		#~ print(text)
		self.SetItemText(text, self.GetSelectedFocusedItem())
	ntf_handler(LVN_ENDLABELEDIT)(OnEndLabelEdit)

class MyForm(form.Form):
	_window_icon_ = blinkyIcon
	_window_icon_sm_ = blinkyIcon
	_window_background_ = 0

	_window_title_ = 'Test auto column resize'

	def OnCreate(self, event):
		self.aList = MyList(parent = self, orExStyle = WS_EX_CLIENTEDGE)
		self.aList.SetExtendedListViewStyle(0, LVS_EX_FULLROWSELECT | LVS_EX_TWOCLICKACTIVATE | LVS_EX_DOUBLEBUFFER | LVS_EX_AUTOSIZECOLUMNS)
		#~ self.aList.SetExtendedListViewStyle(0, LVS_EX_FLATSB|LVS_EX_FULLROWSELECT)
		#~ InitializeFlatSB(self.aList.m_handle)
		self.aList.InsertColumns(columnDefs)
		for i in range(100):
			self.aList.InsertRow(i, ['c o l u m n 0 %d' % i, 'c o l u m n 1 %d' % i])

		self.controls.Add(form.CTRL_VIEW, self.aList)

	def OnDestroy(self, event):
		application.Quit()
	msg_handler(WM_DESTROY)(OnDestroy)

	def OnBeginLabelEdit(self, event):
		print('OnBeginLabelEdit %d' % self.aList.GetSelectedFocusedItem())
		hEdit = self.aList.GetEditControl()
		#~ nmldi = NMLVDISPINFO.from_address(int(event.lParam))
		#~ print('Edit item %d' % nmldi.item[0].iItem)
		return False
		#~ return True
	#~ ntf_handler(LVN_BEGINLABELEDIT)(OnBeginLabelEdit)

	def OnEndLabelEdit(self, event):
		print('OnEndLabelEdit %d' % self.aList.GetSelectedFocusedItem())
		text_size = 1024
		if UNICODE:
			text = type_unicode('\0') * text_size
		else:
			text = type_str('\0') * text_size
		hEdit = self.aList.GetEditControl()
		GetWindowText(hEdit, text, text_size)
		#~ nmldi = NMLVDISPINFO.from_address(int(event.lParam))
		#~ print('Edit item %d' % nmldi.item[0].iItem)
		#~ print(text)
		self.aList.SetItemText(text, self.aList.GetSelectedFocusedItem())
	#~ ntf_handler(LVN_ENDLABELEDIT)(OnEndLabelEdit)

if __name__ == '__main__':
	mainForm = MyForm(rcPos = RECT(0, 0, 320, 240))        
	mainForm.ShowWindow()

	application = Application()
	application.Run()
