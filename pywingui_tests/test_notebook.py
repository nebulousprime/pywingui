## Copyright (c) 2012 Maxim Kolosov

from pywingui.windows import *
from pywingui.wtl import *
from pywingui.lib import form, list, notebook
from pywingui.comctl import ICC_LISTVIEW_CLASSES, ICC_TAB_CLASSES, InitCommonControls

InitCommonControls(ICC_LISTVIEW_CLASSES | ICC_TAB_CLASSES)

class MyForm(form.Form):
	_window_icon_ = Icon('cow.ico')
	_window_icon_sm_ = _window_icon_
	_window_title_ = 'Notebook test'

	def OnCreate(self, event):
		columnDefs = [('column 0', 100), ('column 1', 150)]
		note = notebook.NoteBook(parent = self)
		child_list1 = list.List(parent = note, orExStyle = WS_EX_CLIENTEDGE)
		child_list1.InsertColumns(columnDefs)
		for i in range(100):
			child_list1.InsertRow(i, ['COLUMN 0 %d' % i, 'COLUMN 1 %d' % i])
		child_list2 = list.List(parent = note, orExStyle = WS_EX_CLIENTEDGE)
		child_list2.InsertColumns(columnDefs)
		for i in range(100):
			child_list2.InsertRow(i, ['column 0 %d' % i, 'column 1 %d' % i])
		note.AddTab(0, 'First note', child_list1)
		note.AddTab(1, 'Second note', child_list2)
		note.SetCurrentTab(0)
		self.controls.Add(form.CTRL_VIEW, note)

	msg_handler(WM_CREATE)(OnCreate)

if __name__ == '__main__':
	mainForm = MyForm()        
	mainForm.ShowWindow()

	application = Application()
	application.Run()
