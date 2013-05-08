'XPM file to Icon hexadecimal data; XPM data to Icon; hexadecimal data to Icon'

exit_xpm_data = ("32 32 6 1",
" 	c None",
"!	c black",
"#	c #0000FF",
"$	c #800080",
"%	c #FF0000",
"&	c #808080",
"            ################### ",
"           ###################$$",
"           ##                $$$",
"           ##               $$$$",
"           ##              $$ $$",
"         %%##             $$  $$",
"         %%%#            $$   $$",
"           %%           $$    $$",
"           #%%         $$     $$",
"           ##%%       $$      $$",
"           ## %%     $$       $$",
"%%%%%%%%%%%%%%%%%    $$       $$",
"%%%%%%%%%%%%%%%%%%   $$       $$",
"%%%%%%%%%%%%%%%%%    $$       $$",
"           ## %%     $$       $$",
"           ##%%      $$       $$",
"           #%%       $$       $$",
"           %%        $$  &    $$",
"         %%%#        $$ &&    $$",
"         %%##        $$&&     $$",
"           ##        $$&      $$",
"           ##        $$       $$",
"           ##        $$       $$",
"           ##        $$      $$#",
"           ##########$$#####$$##",
"            #########$$####$$## ",
"                     $$   $$    ",
"                     $$  $$     ",
"                     $$ $$      ",
"                     $$$$       ",
"                     $$$        ",
"                     $$         ")

paper_edit_hex_data = '''
0x00000000,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF0000FF,0x00000000,0x00000000,0x00000000,0x00000000,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF0000FF,0xFF0000FF,0x00000000,0x00000000,0x00000000,
0xFF00FF00,0x00000000,0xFFF0F000,0xFFF0F000,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF0000FF,0xFF0000FF,0xFF0000FF,0x00000000,0x00000000,
0xFF00FF00,0x00000000,0xFFF0F000,0xFF800080,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0xFF0000FF,0xFF0000FF,0xFF0000FF,0xFF0000FF,0x00000000,
0xFF00FF00,0x00000000,0xFFF0F000,0xFFF0F000,0xFF800080,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0xFF0000FF,0xFF0000FF,0xFF0000FF,0xFF0000FF,0xFF0000FF,
0xFF00FF00,0x00000000,0xFFF0F000,0xFFF0F000,0x00000000,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0xFFF0F000,0xFFF0F000,0x00000000,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0xFFF0F000,0xFFF0F000,0x00000000,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0xFFF0F000,0xFFF0F000,0x00000000,0xFF800080,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF800080,0xFF800080,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF800080,0xFF800080,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF800080,0x00000000,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF090909,0x00000000,0xFF00FF00,
0xFF00FF00,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0x00000000,0xFF00FF00,
0x00000000,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0xFF00FF00,0x00000000'''

import os
from math import pow, sqrt

from pywingui import comctl
from pywingui.comdlg import OPENFILENAME_SIZE_VERSION_400, OFN_ALLOWMULTISELECT, OFN_ENABLESIZING, OFN_OVERWRITEPROMPT, OFN_EXPLORER, OPENFILENAME, GetOpenFileName, OpenFileDialog, SaveFileDialog

from pywingui.wtl import *
from pywingui.gdi import CreateBitmap, DeleteObject, CLR_NONE, CLR_DEFAULT
from pywingui.lib import form, coolbar

simple_colors = {'None':'0x00FFFFFF', 'black':'0xFF000000', 'white':'0xFFFFFFFF', 'red':'0xFFFF0000', 'green':'0xFF00FF00', 'blue':'0xFF0000FF'}

def xpm_color_to_hex(value):
	if value in ('None', 'black', 'white', 'red', 'green', 'blue'):
		return simple_colors[value]
	elif value[0] == '#':
		return value.replace('#', '0xFF')
	else:
		return value

def text_to_data(text_data = ''):
	icon_data = text_data.replace('\n', '').split(',')
	icon_size = len(icon_data)
	w = h = int(sqrt(icon_size))
	icon_bits = (c_ulong * icon_size)()
	for i in range(icon_size):
		icon_bits[i] = DWORD(long(float.fromhex(icon_data[i])))
	return icon_bits, w, h

def xpm_data_to_hex(xpm_data = ''):
	str_params = tuple(xpm_data[0].split(' '))
	w, h, clrs, bts = int(str_params[0]), int(str_params[1]), int(str_params[2]), int(str_params[3])
	#hex_data = (c_ulong * pow(w, 2))()
	hex_data = (c_ulong * (w * h))()
	colors = {}
	i = 0
	for line in xpm_data[1:]:
		if line.find('\t') != -1:# COLOR
			key, value = line.split('\t')
			colors[key] = c_ulong(long(float.fromhex(xpm_color_to_hex(value.replace('c ', '')))))
		elif line.find('\t') == -1:# DATA BITS
			for symbol in line:
				if symbol in colors:
					hex_data[i] = colors[symbol]
				else:
					hex_data[i] = c_ulong(0)
				i += 1
	return hex_data, w, h

def icon_from_data(icon_bits, width = 32, height = 32):
	hBitmap = CreateBitmap(width, height, 1, 32, icon_bits)
	hMonoBitmap = CreateBitmap(width, height, 1, 32, None)
	ii = ICONINFO()
	ii.hbmMask = hMonoBitmap
	ii.hbmColor = hBitmap
	hIcon = CreateIconIndirect(ii)
	DeleteObject(hBitmap)
	DeleteObject(hMonoBitmap)
	return hIcon

def hex_to_bitmap(hex_data, width = 32, height = 32):
	return CreateBitmap(width, height, 1, 32, hex_data)

def hex_to_icon(hex_data, width = 32, height = 32):
	return icon_from_data(hex_data, width, height)

bits_exit, w, h = xpm_data_to_hex(exit_xpm_data)
iml = comctl.ImageList(w, h, comctl.ILC_COLOR32 | comctl.ILC_MASK, 0, 64)
bmp_color = hex_to_bitmap(bits_exit, w, h)
bmp_mask = hex_to_bitmap(bits_exit, w, h)
iml.Add(bmp_color, bmp_mask)
iml.AddIconsFromModule('shell32.dll', w, h, LR_LOADMAP3DCOLORS)
#~ iml.SetBkColor(CLR_NONE)#CLR_DEFAULT
DeleteObject(bmp_color)
DeleteObject(bmp_mask)

class MyForm(form.Form):
	#~ _window_icon_ = hex_to_icon(*xpm_data_to_hex(exit_xpm_data))
	_window_icon_ = icon_from_data(*text_to_data(paper_edit_hex_data))
	_window_icon_sm_ = _window_icon_
	_window_background_ = 0 #prevents windows from redrawing background, prevent flicker
	_window_class_style_ = CS_HREDRAW | CS_VREDRAW#make windows invalidate window on resize
	_window_title_ = __doc__
	_form_menu_ = None

	current_path = os.getcwd()

	def create_tool_tips(self, tool_bar):
		tt = comctl.ToolTips(parent = tool_bar)
		tt.SetMaxTipWidth()
		tt.add_tools(tool_bar, ((0, u'Open XPM file'), (2, u'Save TXT file'), (4, u'Exit from application')))
		return tt

	def OnCreate(self, event):
		cool_bar = coolbar.CoolBar(parent = self)
		tool_bar = coolbar.ToolBar(parent = cool_bar, orStyle = comctl.TBSTYLE_TOOLTIPS)
		tool_bar.AddString(u'Open XPM\0Save TXT\0Exit\0')
		#~ tool_bar.SendMessage(comctl.TB_ADDSTRING, 0, u'Open\0Save\0Exit\0')
		#~ tool_bar.SetExtendedStyle(comctl.TBSTYLE_EX_MIXEDBUTTONS)
		#~ tool_bar.add_bitmap(comctl.IDB_STD_LARGE_COLOR)
		#~ tool_bar.add_bitmap(hex_to_bitmap(*xpm_data_to_hex(exit_xpm_data)), 0)
		#~ tool_bar.SendMessage(comctl.CCM_SETVERSION, 5)
		tool_bar.SetImageList(iml)
		#~ print iml.GetImageCount()
		#~ tool_bar.SetButtonSize(32, 32)
		idb = 0
		#~ tool_bar.SetButtonToolTip(0, 'Open XPM file')
		tool_bar.insert_button(form.ID_OPEN, 0, idb, comctl.STD_FILEOPEN);idb += 1
		tool_bar.insert_button(id_button = idb, fs_style = comctl.TBSTYLE_SEP);idb += 1
		tool_bar.insert_button(form.ID_SAVE, 1, idb, comctl.STD_FILESAVE);idb += 1
		tool_bar.insert_button(id_button = idb, fs_style = comctl.TBSTYLE_SEP);idb += 1
		tool_bar.insert_button(form.ID_CLOSE, 2, idb, 0)#comctl.STD_DELETE
		# ======== TOOL TIPS
		tool_bar.SetToolTips(self.create_tool_tips(tool_bar))
		# =========
		cool_bar.SetRedraw(False)
		cool_bar.AddSimpleRebarBandCtrl(tool_bar)
		cool_bar.SetRedraw(True)
		self.controls.Add(tool_bar)
		self.controls.Add(form.CTRL_COOLBAR, cool_bar)

		self.output_text = comctl.Edit(parent = self, style = WS_VISIBLE | WS_CHILD | WS_CLIPCHILDREN | WS_CLIPSIBLINGS, orStyle = WS_EX_CLIENTEDGE | WS_HSCROLL | WS_VSCROLL | ES_MULTILINE | ES_AUTOHSCROLL | ES_AUTOVSCROLL | ES_WANTRETURN)
		self.controls.Add(form.CTRL_VIEW, self.output_text)

		self.status_bar = comctl.StatusBar(parent = self)
		self.controls.Add(form.CTRL_STATUSBAR, self.status_bar)

	def xpm_to_icon_data(self, xpm_path = ''):
		if os.path.isfile(xpm_path):
			f = open(xpm_path, 'r')
			image_parameters = ()
			colors = {}
			output_text_value = 'image_parameters = ()\r\n'
			i = 0
			for line in f.readlines():
				i += 1
				if line[:2] == '/*':
					continue
				elif line[:29] == 'static const unsigned char * ':
					output_text_value += line.replace('static const unsigned char * ', '').replace('[]', '').replace('{', "'''")
				elif i == 3:
					image_parameters = tuple(line.replace('"', '').replace(',\n', '').split(' '))
				elif line.find('\t') != -1:# COLOR
					key, value = line.replace('"', '').replace(',\n', '').split('\t')
					colors[key] = xpm_color_to_hex(value.replace('c ', ''))
				elif line.find('\t') == -1:
					for symbol in line:
						if symbol in colors:
							output_text_value += '%s,' % colors[symbol]
					output_text_value += '\r\n'
			f.close()
			output_text_value = output_text_value.rstrip(',\r\n')
			output_text_value += "'''"
			output_text_value = output_text_value.replace('image_parameters = ()\r\n', 'image_parameters = %s\r\n' % repr(image_parameters))
			self.output_text.SetText(output_text_value)

	def OnOpen(self, event):
		dlg = OpenFileDialog()
		dlg.lpstrInitialDir = self.current_path
		dlg.SetFilter('Icon file(*.xpm)|*.xpm|All files(*.*)|*.*')
		if dlg.DoModal(parent = self):
			self.current_path = dlg.lpstrFile
			self.xpm_to_icon_data(self.current_path)
	cmd_handler(form.ID_OPEN)(OnOpen)

	def OnSave(self, event):
		dlg = SaveFileDialog()
		#~ dlg.lpstrInitialDir = self.current_path
		#~ dlg.lpTemplateName = self.current_path.replace('.ico', '.txt')
		dlg.SetFilter('Icon data file(*.txt)|*.txt')
		if dlg.DoModal(self, self.current_path.replace('.xpm', '.txt')):
			is_save = True
			if os.path.isfile(dlg.lpstrFile):
				if IDNO == MessageBox(self.handle, 'File exists. You want replace it?', 'Question', MB_YESNO | MB_ICONQUESTION):
					is_save = False
			if is_save:
				f = open(dlg.lpstrFile, 'w')
				f.write(self.output_text.GetText().replace('\r', ''))
				f.close()
	cmd_handler(form.ID_SAVE)(OnSave)


if __name__ == '__main__':
	mainForm = MyForm(rcPos = RECT(0, 0, 640, 480))        
	mainForm.ShowWindow()

	application = Application()
	application.Run()
