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

from windows import *
from wtl import *
from sdkddkver import _WIN32_IE, _WIN32_WINNT, NTDDI_VERSION, NTDDI_LONGHORN
from winuser import SetWindowText

ATL_IDW_BAND_FIRST = 0xEB00
HTREEITEM = HANDLE
HIMAGELIST = HANDLE

UINT_MAX = (1l << 32)

ODT_HEADER   = 100
ODT_TAB      = 101
ODT_LISTVIEW = 102

#====== Ranges for control message IDs =================

LVM_FIRST = 0x1000 # ListView messages
TV_FIRST  = 0x1100 # TreeView messages
HDM_FIRST = 0x1200 # Header messages
TCM_FIRST = 0x1300 # Tab control messages

if WINVER >= 0x0400:
	PGM_FIRST = 0x1400 # Pager control messages

	if WINVER >= 0x0501:
		ECM_FIRST = 0x1500 # Edit control messages
		BCM_FIRST = 0x1600 # Button control messages
		CBM_FIRST = 0x1700 # Combobox control messages

	CCM_FIRST      = 0x2000 # Common control shared messages
	CCM_LAST       = (CCM_FIRST + 0x200)
	CCM_SETBKCOLOR = (CCM_FIRST + 1) # lParam is bkColor
	CCM_SETCOLORSCHEME   = (CCM_FIRST + 2) # lParam is color scheme
	CCM_GETCOLORSCHEME   = (CCM_FIRST + 3) # fills in COLORSCHEME pointed to by lParam
	CCM_GETDROPTARGET    = (CCM_FIRST + 4)
	CCM_SETUNICODEFORMAT = (CCM_FIRST + 5)
	CCM_GETUNICODEFORMAT = (CCM_FIRST + 6)

LVCF_FMT     =1
LVCF_WIDTH   =2
LVCF_TEXT    =4
LVCF_SUBITEM =8
LVCF_IMAGE= 16
LVCF_ORDER= 32

TVIF_TEXT    = 1
TVIF_IMAGE   =2
TVIF_PARAM   =4
TVIF_STATE   =8
TVIF_HANDLE = 16
TVIF_SELECTEDIMAGE  = 32
TVIF_CHILDREN      =  64
TVIF_INTEGRAL      =  0x0080
TVIF_DI_SETITEM    =  0x1000

LVIF_TEXT   = 1
LVIF_IMAGE  = 2
LVIF_PARAM  = 4
LVIF_STATE  = 8
LVIF_DI_SETITEM =  0x1000

CBEMAXSTRLEN = 260

class MaskedStructureType(Structure.__class__):
	def __new__(cls, name, bases, dct):
		fields = []
		for field in dct['_fields_']:
			fields.append((field[0], field[1]))
			if len(field) == 4: #masked field
				dct[field[3]] = property(None, lambda self, val, field = field: self.setProperty(field[0], field[2], val))
		dct['_fields_'] = fields
		return Structure.__class__.__new__(cls, name, bases, dct)

class MaskedStructure(Structure):
	__metaclass__ = MaskedStructureType
	_fields_ = []

	def setProperty(self, name, mask, value):
		setattr(self, self._mask_, getattr(self, self._mask_) | mask)
		setattr(self, name, value)

	def clear(self):
		setattr(self, self._mask_, 0)

class NMCBEENDEDIT(Structure):
	_fields_ = [('hdr', NMHDR),
	('fChanged', BOOL),
	('iNewSelection', INT)]
	if UNICODE:
		_fields_ += [('szText', c_wchar_p * CBEMAXSTRLEN), ('iWhy', INT)]
	else:
		_fields_ += [('szText', c_char_p * CBEMAXSTRLEN), ('iWhy', INT)]

class LVCOLUMN(MaskedStructure):
	_mask_ = 'mask'
	_fields_ = [('mask', UINT),
	('fmt', INT, LVCF_FMT, 'format'),
	('cx', INT, LVCF_WIDTH, 'width')]
	if UNICODE:
		_fields_.append(('pszText', c_wchar_p, LVCF_TEXT, 'text'))
	else:
		_fields_.append(('pszText', c_char_p, LVCF_TEXT, 'text'))
	_fields_ += [('cchTextMax', INT),
	('iSubItem', INT),
	('iImage', INT),
	('iOrder', INT)]

class LVITEM(Structure):
	_fields_ = [('mask', UINT),
	('iItem', INT),
	('iSubItem', INT),
	('state', UINT),
	('stateMask', UINT)]
	if UNICODE:
		_fields_.append(('pszText', c_wchar_p))
	else:
		_fields_.append(('pszText', c_char_p))
	_fields_ += [('cchTextMax', INT),
	('iImage', INT),
	('lParam', LPARAM),
	('iIndent', INT)]

class TVITEMEX(MaskedStructure):
	_mask_ = 'mask'
	_fields_ = [('mask', UINT),
	('hItem', HTREEITEM),
	('state', UINT),
	('stateMask', UINT)]
	if UNICODE:
		_fields_.append(('pszText', c_wchar_p, TVIF_TEXT, 'text'))
	else:
		_fields_.append(('pszText', c_char_p, TVIF_TEXT, 'text'))
	_fields_ += [('cchTextMax', INT),
	('iImage', INT, TVIF_IMAGE, 'image'),
	('iSelectedImage', INT, TVIF_SELECTEDIMAGE, 'selectedImage'),
	('cChildren', INT, TVIF_CHILDREN, 'children'),
	('lParam', LPARAM, TVIF_PARAM, 'param'),
	('iIntegral', INT)]

class TVITEM(Structure):
	_fields_ = [('mask', UINT),
	('hItem', HTREEITEM),
	('state', UINT),
	('stateMask', UINT)]
	if UNICODE:
		_fields_.append(('pszText', c_wchar_p))
	else:
		_fields_.append(('pszText', c_char_p))
	_fields_ += [('cchTextMax', INT),
	('iImage', INT),
	('iSelectedImage', INT),
	('cChildren', INT),
	('lParam', LPARAM)]

class TBBUTTON(Structure):
	_fields_ = [('iBitmap', INT),
	('idCommand', INT),
	('fsState', BYTE),
	('fsStyle', BYTE),
	('bReserved', BYTE * 2),
	('dwData', DWORD_PTR),
	('iString', INT_PTR)]

class TBBUTTONINFO(Structure):
	_fields_ = [('cbSize', UINT),
	('dwMask', DWORD),
	('idCommand', INT),
	('iImage', INT),
	('fsState', BYTE),
	('fsStyle', BYTE),
	('cx', WORD),
	('lParam', DWORD_PTR)]
	if UNICODE:
		_fields_ += [('pszText', c_wchar_p), ('cchText', INT)]
	else:
		_fields_ += [('pszText', c_char_p), ('cchText', INT)]

class TVINSERTSTRUCT(Structure):
	_fields_ = [('hParent', HTREEITEM),
	('hInsertAfter', HTREEITEM),
	('itemex', TVITEMEX)]

class TCITEM(Structure):
	_fields_ = [('mask', UINT),
	('dwState', DWORD),
	('dwStateMask', DWORD)]
	if UNICODE:
		_fields_.append(('pszText', c_wchar_p))
	else:
		_fields_.append(('pszText', c_char_p))
	_fields_ += [('cchTextMax', INT),
	('iImage', INT),
	('lParam', LPARAM)]

class NMTREEVIEW(Structure):
	_fields_ = [('hdr', NMHDR),
	('action', UINT),
	('itemOld', TVITEM),
	('itemNew', TVITEM),
	('ptDrag', POINT)]

class NMLISTVIEW(Structure):
	_fields_ = [('hrd', NMHDR),
	('iItem', INT),
	('iSubItem', INT),
	('uNewState', UINT),
	('uOldState', UINT),
	('uChanged', UINT),
	('ptAction', POINT),
	('lParam', LPARAM)]

class INITCOMMONCONTROLSEX(Structure):
	_fields_ = [('dwSize', DWORD), ('dwICC', DWORD)]

class REBARINFO(Structure):
	_fields_ = [('cbSize', UINT),
	('fMask', UINT),
	('himl', HIMAGELIST)]

class REBARBANDINFO(Structure):
	_fields_ = [('cbSize', UINT),
	('fMask', UINT),
	('fStyle', UINT),
	('clrFore', COLORREF),
	('clrBack', COLORREF)]
	if UNICODE:
		_fields_.append(('lpText', c_wchar_p))
	else:
		_fields_.append(('lpText', c_char_p))
	_fields_ += [('cch', UINT),
	('iImage', INT),
	('hwndChild', HWND),
	('cxMinChild', UINT),
	('cyMinChild', UINT),
	('cx', UINT),
	('hbmBack', HBITMAP),
	('wID', UINT),
	('cyChild', UINT),
	('cyMaxChild', UINT),
	('cyIntegral', UINT),
	('cxIdeal', UINT),
	('lParam', LPARAM),
	('cxHeader', UINT)]

class NMTOOLBAR(Structure):
	_fields_ = [('hdr', NMHDR),
	('iItem', INT),
	('tbButton', TBBUTTON),
	('cchText', INT),
	('pszText', LPTSTR),
	('rcButton', RECT)]

class NMTBHOTITEM(Structure):
	_fields_ = [('hdr', NMHDR),
	('idOld', INT),
	('idNew', INT),
	('dwFlags', DWORD)]

class TBADDBITMAP(Structure):
	_fields_ = [('hInst', c_void_p), ('nID', c_void_p)]

class PBRANGE(Structure):
	_fields_ = [('iLow', INT), ('iHigh', INT)]

class NMITEMACTIVATE(Structure):
	_fields_ = [('hdr', NMHDR),
	('iItem', c_int),
	('iSubItem', c_int),
	('uNewState', UINT),
	('uOldState', UINT),
	('uChanged', UINT),
	('ptAction', POINT),
	('lParam', LPARAM),
	('uKeyFlags', UINT)]

class LVHITTESTINFO(Structure):
	_fields_ = [('pt', POINT),
	('flags', c_uint),
	('iItem', c_int),
	('iSubItem', c_int)]
	if _WIN32_WINNT >= 0x0600:
		_fields_.append(('iGroup', c_int))
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return '%s %d %d %d' % (repr(self.pt), self.flags, self.iItem, self.iSubItem)

NM_FIRST = UINT_MAX

SBS_BOTTOMALIGN = 4
SBS_HORZ = 0
SBS_LEFTALIGN = 2
SBS_RIGHTALIGN = 4
SBS_SIZEBOX = 8
SBS_SIZEBOXBOTTOMRIGHTALIGN = 4
SBS_SIZEBOXTOPLEFTALIGN = 2
SBS_SIZEGRIP = 16
SBS_TOPALIGN = 2
SBS_VERT = 1

#====== COMMON CONTROL STYLES
CCS_TOP = 0x00000001L
CCS_NOMOVEY = 0x00000002L
CCS_BOTTOM = 0x00000003L
CCS_NORESIZE = 0x00000004L
CCS_NOPARENTALIGN = 0x00000008L
CCS_ADJUSTABLE = 0x00000020L
CCS_NODIVIDER = 0x00000040L
if _WIN32_IE >= 0x0300:
	CCS_VERT = 0x00000080L
	CCS_LEFT = (CCS_VERT | CCS_TOP)
	CCS_RIGHT = (CCS_VERT | CCS_BOTTOM)
	CCS_NOMOVEX = (CCS_VERT | CCS_NOMOVEY)

RBBS_BREAK     = 0x00000001 # break to new line
RBBS_FIXEDSIZE = 0x00000002 # band can't be sized
RBBS_CHILDEDGE = 0x00000004 # edge around top & bottom of child window
RBBS_HIDDEN    = 0x00000008 # don't show
RBBS_NOVERT    = 0x00000010 # don't show when vertical
RBBS_FIXEDBMP  = 0x00000020 # bitmap doesn't move during band resize
if _WIN32_IE >= 0x0400:
	RBBS_VARIABLEHEIGHT = 0x00000040 # allow autosizing of this child vertically
	RBBS_GRIPPERALWAYS  = 0x00000080 # always show the gripper
	RBBS_NOGRIPPER      = 0x00000100 # never show the gripper
	if _WIN32_IE >= 0x0500:
		RBBS_USECHEVRON = 0x00000200 # display drop-down button for this band if it's sized smaller than ideal width
		if _WIN32_IE >= 0x0501:
			RBBS_HIDETITLE = 0x00000400 # keep band title hidden
			RBBS_TOPALIGN  = 0x00000800 # keep band in top row

RBS_TOOLTIPS = 256
RBS_VARHEIGHT = 512
RBS_BANDBORDERS = 1024
RBS_FIXEDORDER = 2048

RBS_REGISTERDROP = 4096
RBS_AUTOSIZE = 8192
RBS_VERTICALGRIPPER = 16384
RBS_DBLCLKTOGGLE = 32768

RBN_FIRST	= ((UINT_MAX) - 831)
RBN_HEIGHTCHANGE = RBN_FIRST

TBSTYLE_FLAT = 2048
TBSTYLE_LIST = 4096
TBSTYLE_DROPDOWN = 8
TBSTYLE_TRANSPARENT = 0x8000
TBSTYLE_REGISTERDROP = 0x4000
TBSTYLE_BUTTON = 0x0000
TBSTYLE_AUTOSIZE = 0x0010

TB_BUTTONSTRUCTSIZE = WM_USER + 30
TB_ADDBUTTONS = WM_USER + 20

TB_SETBUTTONINFO = WM_USER + 64
TB_INSERTBUTTON = WM_USER + 67
TB_ADDSTRING = WM_USER + 77
if not UNICODE:
	TB_INSERTBUTTON = WM_USER + 21
	TB_ADDSTRING = WM_USER + 28
	TB_SETBUTTONINFO = WM_USER + 66


TB_ENABLEBUTTON = WM_USER + 1
TB_CHECKBUTTON = WM_USER + 2
TB_PRESSBUTTON = WM_USER + 3
TB_HIDEBUTTON = WM_USER + 4
TB_INDETERMINATE = WM_USER + 5
if _WIN32_IE >= 0x0400:
	TB_MARKBUTTON = WM_USER + 6
TB_ISBUTTONENABLED = WM_USER + 9
TB_ISBUTTONCHECKED = WM_USER + 10
TB_ISBUTTONPRESSED = WM_USER + 11
TB_ISBUTTONHIDDEN = WM_USER + 12
TB_ISBUTTONINDETERMINATE = WM_USER + 13
if _WIN32_IE >= 0x0400:
	TB_ISBUTTONHIGHLIGHTED = WM_USER + 14
TB_SETSTATE = WM_USER + 17
TB_GETSTATE = WM_USER + 18
TB_ADDBITMAP = WM_USER + 19

TB_BUTTONCOUNT = WM_USER + 24
TB_GETITEMRECT = WM_USER + 29
TB_SETIMAGELIST = WM_USER + 48
TB_SETDRAWTEXTFLAGS = WM_USER + 70
TB_PRESSBUTTON = WM_USER + 3
TB_GETRECT = WM_USER + 51
TB_SETHOTITEM = WM_USER + 72
TB_HITTEST = WM_USER + 69
TB_GETHOTITEM = WM_USER + 7
TB_SETBUTTONSIZE = WM_USER + 31
TB_AUTOSIZE = WM_USER + 33

TVIF_TEXT = 1
TVIF_IMAGE = 2
TVIF_PARAM = 4
TVIF_STATE = 8
TVIF_HANDLE = 16
TVIF_SELECTEDIMAGE = 32
TVIF_CHILDREN = 64
TVIF_INTEGRAL = 0x0080
TVIF_DI_SETITEM = 0x1000

TVI_ROOT = 0xFFFF0000l
TVI_FIRST = 0xFFFF0001l
TVI_LAST = 0xFFFF0002l
TVI_SORT = 0xFFFF0003l

TVGN_CHILD = 4
TVGN_NEXT = 1
TVGN_ROOT = 0
TVGN_CARET = 0x0009

TVIS_FOCUSED = 1
TVIS_SELECTED = 2
TVIS_CUT = 4
TVIS_DROPHILITED = 8
TVIS_BOLD = 16
TVIS_EXPANDED = 32
TVIS_EXPANDEDONCE = 64
TVIS_OVERLAYMASK = 0xF00
TVIS_STATEIMAGEMASK = 0xF000
TVIS_USERMASK = 0xF000

TV_FIRST = 0x1100
TVM_INSERTITEMA =     TV_FIRST
TVM_INSERTITEMW =    (TV_FIRST+50)
TVM_INSERTITEM = TVM_INSERTITEMA
TVM_SETIMAGELIST =    (TV_FIRST+9)
TVM_DELETEITEM   =   (TV_FIRST+1)
TVM_GETNEXTITEM   =   (TV_FIRST+10)
TVM_EXPAND =   (TV_FIRST+2)
TVM_GETITEMSTATE=        (TV_FIRST + 39)
TVM_ENSUREVISIBLE=       (TV_FIRST + 20)
TVM_SELECTITEM=          (TV_FIRST + 11)
TVM_SETITEMA=            (TV_FIRST + 13)
TVM_SETITEMW =           (TV_FIRST + 63)
TVM_SETITEM= TVM_SETITEMA
TVM_GETITEMA=            (TV_FIRST + 12)
TVM_GETITEMW =           (TV_FIRST + 62)
TVM_GETITEM = TVM_GETITEMA

TVS_HASBUTTONS =       1
TVS_HASLINES = 2
TVS_LINESATROOT =      4
TVS_EDITLABELS  =      8
TVS_DISABLEDRAGDROP =  16
TVS_SHOWSELALWAYS =   32
TVS_CHECKBOXES =  256
TVS_TOOLTIPS = 128
TVS_RTLREADING = 64
TVS_TRACKSELECT = 512
TVS_FULLROWSELECT = 4096
TVS_INFOTIP = 2048
TVS_NONEVENHEIGHT = 16384
TVS_NOSCROLL  = 8192
TVS_SINGLEEXPAND  =1024
TVS_NOHSCROLL   =     0x8000

CBEN_FIRST  =  (UINT_MAX) - 800
CBEN_ENDEDITA = CBEN_FIRST - 5
CBEN_ENDEDITW = CBEN_FIRST - 6
CBEN_ENDEDIT = CBEN_ENDEDITA

# trackbar styles
TBS_AUTOTICKS = 0x0001
TBS_VERT = 0x0002
TBS_HORZ = 0x0000
TBS_TOP = 0x0004
TBS_BOTTOM = 0x0000
TBS_LEFT = 0x0004
TBS_RIGHT = 0x0000
TBS_BOTH = 0x0008
TBS_NOTICKS = 0x0010
TBS_ENABLESELRANGE = 0x0020
TBS_FIXEDLENGTH = 0x0040
TBS_NOTHUMB = 0x0080
TBS_TOOLTIPS = 0x0100
if WINVER >= 0x0500:
	TBS_REVERSED = 0x0200 # Accessibility hint: the smaller number (usually the min value) means "high" and the larger number (usually the max value) means "low"
if WINVER >= 0x0501:
	TBS_DOWNISLEFT = 0x0400 # Down=Left and Up=Right (default is Down=Right and Up=Left)
if WINVER >= 0x0600:
	TBS_NOTIFYBEFOREMOVE = 0x0800 # Trackbar should notify parent before repositioning the slider due to user action (enables snapping)
if NTDDI_VERSION >= NTDDI_LONGHORN:
	TBS_TRANSPARENTBKGND = 0x1000 # Background is painted by the parent via WM_PRINTCLIENT

# trackbar messages
TBM_GETPOS =         (WM_USER)
TBM_GETRANGEMIN =    (WM_USER+1)
TBM_GETRANGEMAX =    (WM_USER+2)
TBM_GETTIC =         (WM_USER+3)
TBM_SETTIC =         (WM_USER+4)
TBM_SETPOS =         (WM_USER+5)
TBM_SETRANGE =       (WM_USER+6)
TBM_SETRANGEMIN =    (WM_USER+7)
TBM_SETRANGEMAX =    (WM_USER+8)
TBM_CLEARTICS =      (WM_USER+9)
TBM_SETSEL =         (WM_USER+10)
TBM_SETSELSTART =    (WM_USER+11)
TBM_SETSELEND =      (WM_USER+12)
TBM_GETPTICS =       (WM_USER+14)
TBM_GETTICPOS =      (WM_USER+15)
TBM_GETNUMTICS =     (WM_USER+16)
TBM_GETSELSTART =    (WM_USER+17)
TBM_GETSELEND =      (WM_USER+18)
TBM_CLEARSEL =       (WM_USER+19)
TBM_SETTICFREQ =     (WM_USER+20)
TBM_SETPAGESIZE =    (WM_USER+21)
TBM_GETPAGESIZE =    (WM_USER+22)
TBM_SETLINESIZE =    (WM_USER+23)
TBM_GETLINESIZE =    (WM_USER+24)
TBM_GETTHUMBRECT =   (WM_USER+25)
TBM_GETCHANNELRECT = (WM_USER+26)
TBM_SETTHUMBLENGTH = (WM_USER+27)
TBM_GETTHUMBLENGTH = (WM_USER+28)
TBM_SETTOOLTIPS =    (WM_USER+29)
TBM_GETTOOLTIPS =    (WM_USER+30)
TBM_SETTIPSIDE =     (WM_USER+31)
TBM_SETBUDDY =       (WM_USER+32) 
TBM_GETBUDDY =       (WM_USER+33) 
if WINVER >= 0x0400:
	TBM_SETUNICODEFORMAT = CCM_SETUNICODEFORMAT
	TBM_GETUNICODEFORMAT = CCM_GETUNICODEFORMAT

# trackbar top-side flags
TBTS_TOP = 0
TBTS_LEFT = 1
TBTS_BOTTOM = 2
TBTS_RIGHT = 3

TB_LINEUP = 0
TB_LINEDOWN = 1
TB_PAGEUP = 2
TB_PAGEDOWN = 3
TB_THUMBPOSITION = 4
TB_THUMBTRACK = 5
TB_TOP = 6
TB_BOTTOM = 7
TB_ENDTRACK = 8

# trackbar custom draw item specs
TBCD_TICS =    0x0001
TBCD_THUMB =   0x0002
TBCD_CHANNEL = 0x0003

TRBN_THUMBPOSCHANGING = 1500

STATUSCLASSNAME = "msctls_statusbar32"

REBARCLASSNAMEA = type_str('ReBarWindow32')
REBARCLASSNAMEW = type_unicode('ReBarWindow32')
REBARCLASSNAME = REBARCLASSNAMEW
if not UNICODE:
	REBARCLASSNAME = REBARCLASSNAMEA

PROGRESS_CLASSA = type_str('msctls_progress32')
PROGRESS_CLASSW = type_unicode('msctls_progress32')
PROGRESS_CLASS = PROGRESS_CLASSW
if not UNICODE:
	PROGRESS_CLASS = PROGRESS_CLASSA

TRACKBAR_CLASSA = type_str('msctls_trackbar32')
TRACKBAR_CLASSW = type_unicode('msctls_trackbar32')
TRACKBAR_CLASS = TRACKBAR_CLASSW
if not UNICODE:
	TRACKBAR_CLASS = TRACKBAR_CLASSA

WC_EDIT = "Edit"
BUTTON = "BUTTON"

WC_STATIC = 'Static'

WC_COMBOBOXA = type_str('ComboBox')
WC_COMBOBOXW = type_unicode('ComboBox')
WC_COMBOBOX = WC_COMBOBOXW
if not UNICODE:
	WC_COMBOBOX = WC_COMBOBOXA

WC_COMBOBOXEXA = type_str('ComboBoxEx32')
WC_COMBOBOXEXW = type_unicode('ComboBoxEx32')
WC_COMBOBOXEX = WC_COMBOBOXEXW
if not UNICODE:
	WC_COMBOBOXEX = WC_COMBOBOXEXA

WC_TREEVIEWA = type_str('SysTreeView32')
WC_TREEVIEWW = type_unicode('SysTreeView32')
WC_TREEVIEW = WC_TREEVIEWW
if not UNICODE:
	WC_TREEVIEW = WC_TREEVIEWA

WC_LISTVIEWA = type_str('SysListView32')
WC_LISTVIEWW = type_unicode('SysListView32')
WC_LISTVIEW = WC_LISTVIEWW
if not UNICODE:
	WC_LISTVIEW = WC_LISTVIEWA

TOOLBARCLASSNAMEA = type_str('ToolbarWindow32')
TOOLBARCLASSNAMEW = type_unicode('ToolbarWindow32')
TOOLBARCLASSNAME = TOOLBARCLASSNAMEW
if not UNICODE:
	TOOLBARCLASSNAME = TOOLBARCLASSNAMEA

WC_TABCONTROLA = type_str('SysTabControl32')
WC_TABCONTROLW = type_unicode('SysTabControl32')
WC_TABCONTROL = WC_TABCONTROLW
if not UNICODE:
	WC_TABCONTROL = WC_TABCONTROLA

LVS_ICON    = 0
LVS_REPORT   = 1
LVS_SMALLICON = 2
LVS_LIST    = 3
LVS_TYPEMASK = 3
LVS_SINGLESEL = 4
LVS_SHOWSELALWAYS = 8
LVS_SORTASCENDING = 16
LVS_SORTDESCENDING = 32
LVS_SHAREIMAGELISTS = 64
LVS_NOLABELWRAP     = 128
LVS_AUTOARRANGE     = 256
LVS_EDITLABELS      = 512
LVS_NOSCROLL = 0x2000
LVS_TYPESTYLEMASK  =  0xfc00
LVS_ALIGNTOP = 0
LVS_ALIGNLEFT =       0x800
LVS_ALIGNMASK  =      0xc00
LVS_OWNERDRAWFIXED =  0x400
LVS_NOCOLUMNHEADER =  0x4000
LVS_NOSORTHEADER   =  0x8000
LVS_OWNERDATA = 4096
LVS_EX_CHECKBOXES = 4
LVS_EX_FULLROWSELECT = 32
LVS_EX_GRIDLINES = 1
LVS_EX_HEADERDRAGDROP = 16
LVS_EX_ONECLICKACTIVATE = 64
LVS_EX_SUBITEMIMAGES = 2
LVS_EX_TRACKSELECT = 8
LVS_EX_TWOCLICKACTIVATE = 128
LVS_EX_FLATSB       = 0x00000100
LVS_EX_REGIONAL     = 0x00000200
LVS_EX_INFOTIP      = 0x00000400
LVS_EX_UNDERLINEHOT = 0x00000800
LVS_EX_UNDERLINECOLD = 0x00001000
LVS_EX_MULTIWORKAREAS = 0x00002000
LVS_EX_LABELTIP     = 0x00004000
LVS_EX_BORDERSELECT = 0x00008000

LVIS_FOCUSED         = 0x0001
LVIS_SELECTED        = 0x0002
LVIS_CUT             = 0x0004
LVIS_DROPHILITED     = 0x0008
LVIS_ACTIVATING      = 0x0020

LVIS_OVERLAYMASK     = 0x0F00
LVIS_STATEIMAGEMASK  = 0xF000

if _WIN32_IE >= 0x0400:
	LV_MAX_WORKAREAS = 16

LVM_FIRST = 0x1000
LVM_GETBKCOLOR = LVM_FIRST
LVM_SETBKCOLOR = LVM_FIRST + 1
LVM_GETIMAGELIST = LVM_FIRST + 2
LVM_SETIMAGELIST = LVM_FIRST + 3
LVM_GETITEMCOUNT = LVM_FIRST + 4
LVM_DELETEITEM = LVM_FIRST + 8
LVM_DELETEALLITEMS = LVM_FIRST + 9
LVM_GETCALLBACKMASK = LVM_FIRST + 10
LVM_SETCALLBACKMASK = LVM_FIRST + 11
LVM_GETNEXTITEM = LVM_FIRST + 12
LVM_GETITEMRECT = LVM_FIRST + 14
LVM_SETITEMPOSITION = LVM_FIRST + 15
LVM_GETITEMPOSITION = LVM_FIRST + 16
LVM_HITTEST = LVM_FIRST + 18
LVM_ENSUREVISIBLE = LVM_FIRST + 19
LVM_SCROLL = LVM_FIRST + 20
LVM_REDRAWITEMS = LVM_FIRST + 21
LVM_ARRANGE = LVM_FIRST + 22
LVM_GETEDITCONTROL = LVM_FIRST + 24
LVM_DELETECOLUMN = LVM_FIRST + 28
LVM_GETCOLUMNWIDTH = LVM_FIRST + 29
LVM_SETCOLUMNWIDTH = LVM_FIRST + 30
LVM_GETHEADER = LVM_FIRST + 31
LVM_CREATEDRAGIMAGE = LVM_FIRST + 33
LVM_GETVIEWRECT = LVM_FIRST + 34
LVM_GETTEXTCOLOR = LVM_FIRST + 35
LVM_SETTEXTCOLOR = LVM_FIRST + 36
LVM_GETTEXTBKCOLOR = LVM_FIRST + 37
LVM_SETTEXTBKCOLOR = LVM_FIRST + 38
LVM_GETTOPINDEX = LVM_FIRST + 39
LVM_GETCOUNTPERPAGE = LVM_FIRST + 40
LVM_GETORIGIN = LVM_FIRST + 41
LVM_UPDATE = LVM_FIRST + 42
LVM_SETITEMSTATE = LVM_FIRST + 43
LVM_GETITEMSTATE = LVM_FIRST + 44
LVM_SETITEMCOUNT = LVM_FIRST + 47
LVM_SORTITEMS = LVM_FIRST + 48
LVM_SETITEMPOSITION32 = LVM_FIRST + 49
LVM_GETSELECTEDCOUNT = LVM_FIRST + 50
LVM_GETITEMSPACING = LVM_FIRST + 51
LVM_SETICONSPACING = LVM_FIRST + 53
LVM_SETEXTENDEDLISTVIEWSTYLE = LVM_FIRST + 54
LVM_GETEXTENDEDLISTVIEWSTYLE = LVM_FIRST + 55
LVM_GETSUBITEMRECT = LVM_FIRST + 56
LVM_SUBITEMHITTEST = LVM_FIRST + 57
LVM_SETCOLUMNORDERARRAY = LVM_FIRST + 58
LVM_GETCOLUMNORDERARRAY = LVM_FIRST + 59
LVM_SETHOTITEM = LVM_FIRST + 60
LVM_GETHOTITEM = LVM_FIRST + 61
LVM_SETHOTCURSOR = LVM_FIRST + 62
LVM_GETHOTCURSOR = LVM_FIRST + 63
LVM_APPROXIMATEVIEWRECT = LVM_FIRST + 64
LVM_SETWORKAREAS = LVM_FIRST + 65
LVM_GETSELECTIONMARK = LVM_FIRST + 66
LVM_SETSELECTIONMARK = LVM_FIRST + 67
LVM_GETWORKAREAS = LVM_FIRST + 70
LVM_SETHOVERTIME = LVM_FIRST + 71
LVM_GETHOVERTIME = LVM_FIRST + 72
LVM_GETNUMBEROFWORKAREAS = LVM_FIRST + 73
LVM_SETTOOLTIPS = LVM_FIRST + 74
LVM_GETITEM = LVM_FIRST + 75
LVM_SETITEM = LVM_FIRST + 76
LVM_INSERTITEM = LVM_FIRST + 77
LVM_GETTOOLTIPS = LVM_FIRST + 78
LVM_SORTITEMSEX = LVM_FIRST + 81
LVM_FINDITEM = LVM_FIRST + 83
LVM_GETSTRINGWIDTH = LVM_FIRST + 87
LVM_GETCOLUMN = LVM_FIRST + 95
LVM_SETCOLUMN = LVM_FIRST + 96
LVM_INSERTCOLUMN = LVM_FIRST + 97
LVM_GETITEMTEXT = LVM_FIRST + 115
LVM_SETITEMTEXT = LVM_FIRST + 116
LVM_GETISEARCHSTRING = LVM_FIRST + 117
LVM_EDITLABEL = LVM_FIRST + 118
LVM_SETBKIMAGE = LVM_FIRST + 138
LVM_GETBKIMAGE = LVM_FIRST + 139

if not UNICODE:
	LVM_GETITEM = LVM_FIRST + 5
	LVM_SETITEM = LVM_FIRST + 6
	LVM_INSERTITEM = LVM_FIRST + 7
	LVM_FINDITEM = LVM_FIRST + 13
	LVM_GETSTRINGWIDTH = LVM_FIRST + 17
	LVM_EDITLABEL = LVM_FIRST + 23
	LVM_GETCOLUMN = LVM_FIRST + 25
	LVM_SETCOLUMN = LVM_FIRST + 26
	LVM_INSERTCOLUMN = LVM_FIRST + 27
	LVM_GETITEMTEXT = LVM_FIRST + 45
	LVM_SETITEMTEXT = LVM_FIRST + 46
	LVM_GETISEARCHSTRING = LVM_FIRST + 52
	LVM_SETBKIMAGE = LVM_FIRST + 68
	LVM_GETBKIMAGE = LVM_FIRST + 69

if _WIN32_WINNT >= 0x0501:
	LVM_GETGROUPSTATE = LVM_FIRST + 92
	LVM_GETFOCUSEDGROUP = LVM_FIRST + 93
	LVM_GETGROUPRECT = LVM_FIRST + 98
	LVM_SETSELECTEDCOLUMN = LVM_FIRST + 140
	LVM_SETVIEW = LVM_FIRST + 142
	LVM_GETVIEW = LVM_FIRST + 143
	LVM_INSERTGROUP = LVM_FIRST + 145
	LVM_SETGROUPINFO = LVM_FIRST + 147
	LVM_GETGROUPINFO = LVM_FIRST + 149
	LVM_REMOVEGROUP = LVM_FIRST + 150
	LVM_MOVEGROUP = LVM_FIRST + 151
	LVM_GETGROUPCOUNT = LVM_FIRST + 152
	LVM_GETGROUPINFOBYINDEX = LVM_FIRST + 153
	LVM_MOVEITEMTOGROUP = LVM_FIRST + 154
	LVM_SETGROUPMETRICS = LVM_FIRST + 155
	LVM_GETGROUPMETRICS = LVM_FIRST + 156
	LVM_ENABLEGROUPVIEW = LVM_FIRST + 157
	LVM_SORTGROUPS = LVM_FIRST + 158
	LVM_INSERTGROUPSORTED = LVM_FIRST + 159
	LVM_REMOVEALLGROUPS = LVM_FIRST + 160
	LVM_HASGROUP = LVM_FIRST + 161
	LVM_SETTILEVIEWINFO = LVM_FIRST + 162
	LVM_GETTILEVIEWINFO = LVM_FIRST + 163
	LVM_SETTILEINFO = LVM_FIRST + 164
	LVM_GETTILEINFO = LVM_FIRST + 165
	LVM_SETINSERTMARK = LVM_FIRST + 166
	LVM_GETINSERTMARK = LVM_FIRST + 167
	LVM_INSERTMARKHITTEST = LVM_FIRST + 168
	LVM_GETINSERTMARKRECT = LVM_FIRST + 169
	LVM_SETINSERTMARKCOLOR = LVM_FIRST + 170
	LVM_GETINSERTMARKCOLOR = LVM_FIRST + 171
	LVM_SETINFOTIP = LVM_FIRST + 173
	LVM_GETSELECTEDCOLUMN = LVM_FIRST + 174
	LVM_ISGROUPVIEWENABLED = LVM_FIRST + 175
	LVM_GETOUTLINECOLOR = LVM_FIRST + 176
	LVM_SETOUTLINECOLOR = LVM_FIRST + 177
	LVM_CANCELEDITLABEL = LVM_FIRST + 179
	LVM_MAPINDEXTOID = LVM_FIRST + 180
	LVM_MAPIDTOINDEX = LVM_FIRST + 181
	LVM_ISITEMVISIBLE = LVM_FIRST + 182
	if _WIN32_WINNT >= 0x0600:
		LVM_GETEMPTYTEXT = LVM_FIRST + 204
		LVM_GETFOOTERRECT = LVM_FIRST + 205
		LVM_GETFOOTERINFO = LVM_FIRST + 206
		LVM_GETFOOTERITEMRECT = LVM_FIRST + 207
		LVM_GETFOOTERITEM = LVM_FIRST + 208
		LVM_GETITEMINDEXRECT = LVM_FIRST + 209
		LVM_SETITEMINDEXSTATE = LVM_FIRST + 210
		LVM_GETNEXTITEMINDEX = LVM_FIRST + 211

LVN_FIRST = (UINT_MAX) - 100
LVN_ITEMCHANGING    =    (LVN_FIRST-0)
LVN_ITEMCHANGED     =    (LVN_FIRST-1)
LVN_INSERTITEM      =    (LVN_FIRST-2)
LVN_DELETEITEM       =   (LVN_FIRST-3)
LVN_DELETEALLITEMS    =  (LVN_FIRST-4)
LVN_BEGINLABELEDIT = LVN_FIRST-75
LVN_ENDLABELEDIT = LVN_FIRST-76
if not UNICODE:
	LVN_BEGINLABELEDIT = LVN_FIRST-5
	LVN_ENDLABELEDIT = LVN_FIRST-6
LVN_COLUMNCLICK       =  (LVN_FIRST-8)
LVN_BEGINDRAG         =  (LVN_FIRST-9)
LVN_BEGINRDRAG        =  (LVN_FIRST-11)

NM_OUTOFMEMORY    = NM_FIRST-1
NM_CLICK          = NM_FIRST-2
NM_DBLCLK         = NM_FIRST-3
NM_RETURN         = NM_FIRST-4
NM_RCLICK         = NM_FIRST-5
NM_RDBLCLK        = NM_FIRST-6
NM_SETFOCUS       = NM_FIRST-7
NM_KILLFOCUS      = NM_FIRST-8
NM_CUSTOMDRAW     = NM_FIRST-12
NM_HOVER          = NM_FIRST-13
NM_NCHITTEST      = NM_FIRST-14
NM_KEYDOWN        = NM_FIRST-15
NM_RELEASEDCAPTURE= NM_FIRST-16
NM_SETCURSOR      = NM_FIRST-17
NM_CHAR           = NM_FIRST-18

LVCFMT_LEFT = 0
LVCFMT_RIGHT = 1
LVCFMT_CENTER = 2
LVCFMT_JUSTIFYMASK = 3
LVCFMT_IMAGE = 2048
LVCFMT_BITMAP_ON_RIGHT = 4096
LVCFMT_COL_HAS_IMAGES = 32768

#~ ICC_LISTVIEW_CLASSES =1
#~ ICC_TREEVIEW_CLASSES =2
#~ ICC_BAR_CLASSES      =4
#~ ICC_TAB_CLASSES      =8
#~ ICC_UPDOWN_CLASS =16
#~ ICC_PROGRESS_CLASS =32
#~ ICC_HOTKEY_CLASS =64
#~ ICC_ANIMATE_CLASS= 128
#~ ICC_WIN95_CLASSES= 255
#~ ICC_DATE_CLASSES =256
#~ ICC_USEREX_CLASSES =512
#~ ICC_COOL_CLASSES =1024
#~ ICC_INTERNET_CLASSES =2048
#~ ICC_PAGESCROLLER_CLASS =4096
#~ ICC_NATIVEFNTCTL_CLASS= 8192
ICC_LISTVIEW_CLASSES = 0x00000001# listview, header
ICC_TREEVIEW_CLASSES = 0x00000002# treeview, tooltips
ICC_BAR_CLASSES = 0x00000004# toolbar, statusbar, trackbar, tooltips
ICC_TAB_CLASSES = 0x00000008# tab, tooltips
ICC_UPDOWN_CLASS = 0x00000010# updown
ICC_PROGRESS_CLASS = 0x00000020# progress
ICC_HOTKEY_CLASS = 0x00000040# hotkey
ICC_ANIMATE_CLASS = 0x00000080# animate
ICC_WIN95_CLASSES = 0x000000FF
ICC_DATE_CLASSES = 0x00000100# month picker, date picker, time picker, updown
ICC_USEREX_CLASSES = 0x00000200# comboex
ICC_COOL_CLASSES = 0x00000400# rebar (coolbar) control
if WINVER >= 0x0400:
	ICC_INTERNET_CLASSES = 0x00000800
	ICC_PAGESCROLLER_CLASS = 0x00001000# page scroller
	ICC_NATIVEFNTCTL_CLASS = 0x00002000# native font control
if WINVER >= 0x0501:
	ICC_STANDARD_CLASSES = 0x00004000
	ICC_LINK_CLASS = 0x00008000

TCN_FIRST = UINT_MAX -550
TCN_LAST = UINT_MAX -580
TCN_KEYDOWN = TCN_FIRST
TCN_SELCHANGE = TCN_FIRST-1
TCN_SELCHANGING = TCN_FIRST-2

TVE_COLLAPSE = 1
TVE_EXPAND = 2
TVE_TOGGLE = 3
TVE_COLLAPSERESET = 0x8000

TCM_FIRST = 0x1300

TCM_GETITEM = TCM_FIRST+60
TCM_INSERTITEM = TCM_FIRST+62
if not UNICODE:
	TCM_GETITEM = TCM_FIRST+5
	TCM_INSERTITEM = TCM_FIRST+7

TCM_ADJUSTRECT = TCM_FIRST+40
TCM_GETCURSEL = TCM_FIRST+11
TCM_SETCURSEL = TCM_FIRST+12

TVN_FIRST = UINT_MAX-400
TVN_LAST = UINT_MAX-499

TVN_ITEMEXPANDING = TVN_FIRST-54
TVN_SELCHANGED = TVN_FIRST-51
TVN_DELETEITEM = TVN_FIRST-58
if not UNICODE:
	TVN_ITEMEXPANDING = TVN_FIRST-5
	TVN_SELCHANGED = TVN_FIRST-2
	TVN_DELETEITEM = TVN_FIRST-9

SB_SIMPLE = WM_USER+9
SB_SETTEXT = WM_USER+11
if not UNICODE:
	SB_SETTEXT = WM_USER+1

SBT_OWNERDRAW = 0x1000
SBT_NOBORDERS = 256
SBT_POPOUT = 512
SBT_RTLREADING = 1024
SBT_TOOLTIPS = 0x0800

TBN_FIRST = UINT_MAX-700
TBN_DROPDOWN = TBN_FIRST - 10
TBN_HOTITEMCHANGE = TBN_FIRST - 13
TBDDRET_DEFAULT = 0
TBDDRET_NODEFAULT = 1
TBDDRET_TREATPRESSED = 2

HINST_COMMCTRL = -1#HINSTANCE - 1

IDB_STD_SMALL_COLOR = 0
IDB_STD_LARGE_COLOR = 1
IDB_VIEW_SMALL_COLOR = 4
IDB_VIEW_LARGE_COLOR = 5
if _WIN32_IE >= 0x0300:
	IDB_HIST_SMALL_COLOR = 8
	IDB_HIST_LARGE_COLOR = 9
if _WIN32_WINNT >= 0x600:
	IDB_HIST_NORMAL = 12
	IDB_HIST_HOT = 13
	IDB_HIST_DISABLED = 14
	IDB_HIST_PRESSED = 15

# icon indexes for standard bitmap
STD_CUT = 0
STD_COPY = 1
STD_PASTE = 2
STD_UNDO = 3
STD_REDOW = 4
STD_DELETE = 5
STD_FILENEW = 6
STD_FILEOPEN = 7
STD_FILESAVE = 8
STD_PRINTPRE = 9
STD_PROPERTIES = 10
STD_HELP = 11
STD_FIND = 12
STD_REPLACE = 13
STD_PRINT = 14

# icon indexes for standard view bitmap
VIEW_LARGEICONS = 0
VIEW_SMALLICONS = 1
VIEW_LIST = 2
VIEW_DETAILS = 3
VIEW_SORTNAME = 4
VIEW_SORTSIZE = 5
VIEW_SORTDATE = 6
VIEW_SORTTYPE = 7
VIEW_PARENTFOLDER = 8
VIEW_NETCONNECT = 9
VIEW_NETDISCONNECT = 10
VIEW_NEWFOLDER = 11
if _WIN32_IE >= 0x0400:
	VIEW_VIEWMENU = 12

if _WIN32_IE >= 0x0300:
	HIST_BACK = 0
	HIST_FORWARD = 1
	HIST_FAVORITES = 2
	HIST_ADDTOFAVORITES = 3
	HIST_VIEWTREE = 4

PBS_SMOOTH = 0x01
PBS_VERTICAL = 0x04

CCM_FIRST = 0x2000 # Common control shared messages
CCM_SETBKCOLOR = CCM_FIRST + 1

PBM_SETRANGE    = (WM_USER+1)
PBM_SETPOS      = (WM_USER+2)
PBM_DELTAPOS    = (WM_USER+3)
PBM_SETSTEP     = (WM_USER+4)
PBM_STEPIT      = (WM_USER+5)
PBM_SETRANGE32  = (WM_USER+6)
PBM_GETRANGE    = (WM_USER+7)
PBM_GETPOS      = (WM_USER+8)
PBM_SETBARCOLOR = (WM_USER+9)
PBM_SETBKCOLOR  = CCM_SETBKCOLOR

LB_ADDSTRING = 384
LB_INSERTSTRING = 385
LB_DELETESTRING = 386
LB_RESETCONTENT = 388
LB_GETCOUNT = 395
LB_SETTOPINDEX = 407

RBBIM_STYLE = 0x00000001
RBBIM_COLORS = 0x00000002
RBBIM_TEXT = 0x00000004
RBBIM_IMAGE = 0x00000008
RBBIM_CHILD = 0x00000010
RBBIM_CHILDSIZE = 0x00000020
RBBIM_SIZE = 0x00000040
RBBIM_BACKGROUND = 0x00000080
RBBIM_ID = 0x00000100
if _WIN32_IE >= 0x0400:
	RBBIM_IDEALSIZE = 0x00000200
	RBBIM_LPARAM = 0x00000400
	RBBIM_HEADERSIZE = 0x00000800 # control the size of the header
if _WIN32_WINNT >= 0x0600:
	RBBIM_CHEVRONLOCATION = 0x00001000
	RBBIM_CHEVRONSTATE = 0x00002000


ImageList_Create = windll.comctl32.ImageList_Create
ImageList_Destroy = windll.comctl32.ImageList_Destroy
ImageList_AddMasked = windll.comctl32.ImageList_AddMasked
ImageList_AddIcon = windll.comctl32.ImageList_AddIcon
ImageList_SetBkColor = windll.comctl32.ImageList_SetBkColor

InitCommonControlsEx = WINFUNCTYPE(c_bool, POINTER(INITCOMMONCONTROLSEX))(('InitCommonControlsEx', windll.comctl32))

def InitCommonControls(dwICC):
	iccex = INITCOMMONCONTROLSEX()
	iccex.dwSize = sizeof(INITCOMMONCONTROLSEX)
	iccex.dwICC = dwICC
	InitCommonControlsEx(iccex)

MAXPROPPAGES = 100

PSP_DEFAULT = 0x00000000
PSP_DLGINDIRECT = 0x00000001
PSP_USEHICON = 0x00000002
PSP_USEICONID = 0x00000004
PSP_USETITLE = 0x00000008
PSP_RTLREADING = 0x00000010

PSP_HASHELP = 0x00000020
PSP_USEREFPARENT = 0x00000040
PSP_USECALLBACK = 0x00000080
PSP_PREMATURE = 0x00000400

#----- New flags for wizard97 --------------
if _WIN32_IE >= 0x0400:
	PSP_HIDEHEADER = 0x00000800
	PSP_USEHEADERTITLE = 0x00001000
	PSP_USEHEADERSUBTITLE = 0x00002000

if _WIN32_WINNT >= 0x0501:
	PSP_USEFUSIONCONTEXT = 0x00004000

if _WIN32_IE >= 0x0500:
	PSPCB_ADDREF = 0
PSPCB_RELEASE = 1
PSPCB_CREATE = 2

#----- PropSheet Header related ---------
PSH_DEFAULT = 0x00000000
PSH_PROPTITLE = 0x00000001
PSH_USEHICON = 0x00000002
PSH_USEICONID = 0x00000004
PSH_PROPSHEETPAGE = 0x00000008

PSH_WIZARDHASFINISH = 0x00000010
PSH_WIZARD = 0x00000020
PSH_USEPSTARTPAGE = 0x00000040
PSH_NOAPPLYNOW = 0x00000080

PSH_USECALLBACK = 0x00000100
PSH_HASHELP = 0x00000200
PSH_MODELESS = 0x00000400
PSH_RTLREADING = 0x00000800

PSH_WIZARDCONTEXTHELP = 0x00001000

#----- New flags for wizard97 -----------
if _WIN32_IE >= 0x0400:
	if _WIN32_IE < 0x0500:
		PSH_WIZARD97 = 0x00002000
	else:
		PSH_WIZARD97 = 0x01000000

	PSH_WATERMARK = 0x00008000

	PSH_USEHBMWATERMARK = 0x00010000 # user pass in a hbmWatermark instead of pszbmWatermark
	PSH_USEHPLWATERMARK = 0x00020000
	PSH_STRETCHWATERMARK = 0x00040000 # stretchwatermark also applies for the header
	PSH_HEADER = 0x00080000

	PSH_USEHBMHEADER = 0x00100000
	PSH_USEPAGELANG = 0x00200000 # use frame dialog template matched to page

#----- New flags for wizard-lite --------
if _WIN32_IE >= 0x0500:
	PSH_WIZARD_LITE = 0x00400000
	PSH_NOCONTEXTHELP = 0x02000000

if _WIN32_WINNT >= 0x0600:
	PSH_AEROWIZARD = 0x00004000
	PSH_RESIZABLE = 0x04000000
	PSH_HEADERBITMAP = 0x08000000
	PSH_NOMARGIN = 0x10000000

HPROPSHEETPAGE = c_void_p
_PROPSHEETPAGE = c_void_p#later initialized as PROPSHEETPAGE

LPFNPSPCALLBACK = WINFUNCTYPE(UINT, HWND, UINT, _PROPSHEETPAGE)

class DUMMYUNIONNAME(Union):
	if UNICODE:
		_fields_ = [('pszTemplate', c_wchar_p), ('pResource', LPDLGTEMPLATE)]
	else:
		_fields_ = [('pszTemplate', c_char_p), ('pResource', LPDLGTEMPLATE)]

class _DUMMYUNIONNAME(Union):
	if UNICODE:
		_fields_ = [('hIcon', HICON), ('pszIcon', c_wchar_p)]
	else:
		_fields_ = [('hIcon', HICON), ('pszIcon', c_char_p)]
DUMMYUNIONNAME2 = _DUMMYUNIONNAME

class PROPSHEETPAGE(Structure):
	_fields_ = [('dwSize', DWORD),
	('dwFlags', DWORD),
	('hInstance', c_void_p),
	('u1', DUMMYUNIONNAME),
	('u2', DUMMYUNIONNAME2)]
	if UNICODE:
		_fields_.append(('pszTitle', c_wchar_p))
	else:
		_fields_.append(('pszTitle', c_char_p))
	_fields_ + [('pfnDlgProc', DLGPROC),
	('lParam', LPARAM),
	('pfnCallback', LPFNPSPCALLBACK),
	('pcRefParent', c_void_p)]
	_anonymous_ = ('u1', 'u2')
_PROPSHEETPAGE = PROPSHEETPAGE
LPCPROPSHEETPAGE = POINTER(PROPSHEETPAGE)

PFNPROPSHEETCALLBACK = WINFUNCTYPE(c_int, HWND, UINT, LPARAM)

class _DUMMYUNIONNAME2(Union):
	if UNICODE:
		_fields_ = [('nStartPage', UINT), ('pStartPage', c_wchar_p)]
	else:
		_fields_ = [('nStartPage', UINT), ('pStartPage', c_char_p)]

class _DUMMYUNIONNAME3(Union):
	_fields_ = [('ppsp', LPCPROPSHEETPAGE), ('phpage', HPROPSHEETPAGE)]

class PROPSHEETHEADER(Structure):
	_fields_ = [('dwSize', DWORD),
	('dwFlags', DWORD),
	('hwndParent', c_void_p),
	('hInstance', c_void_p),
	('u1', _DUMMYUNIONNAME)]
	if UNICODE:
		_fields_.append(('pszCaption', c_wchar_p))
	else:
		_fields_.append(('pszCaption', c_char_p))
	_fields_ += [('nPages', UINT),
	('u2', _DUMMYUNIONNAME2),
	('u3', _DUMMYUNIONNAME3),
	('pfnCallback', PFNPROPSHEETCALLBACK)]
	_anonymous_ = ('u1', 'u2', 'u3')
LPCPROPSHEETHEADER = POINTER(PROPSHEETHEADER)

CreatePropertySheetPage = WINFUNCTYPE(c_void_p, LPCPROPSHEETPAGE)(('CreatePropertySheetPageW', windll.comctl32))
PropertySheet = WINFUNCTYPE(HPROPSHEETPAGE, LPCPROPSHEETHEADER)(('PropertySheetW', windll.comctl32))
if not UNICODE:
	CreatePropertySheetPage = WINFUNCTYPE(c_void_p, LPCPROPSHEETPAGE)(('CreatePropertySheetPageA', windll.comctl32))
	PropertySheet = WINFUNCTYPE(HPROPSHEETPAGE, LPCPROPSHEETHEADER)(('PropertySheetA', windll.comctl32))
DestroyPropertySheetPage = WINFUNCTYPE(c_bool, HPROPSHEETPAGE)(('DestroyPropertySheetPage', windll.comctl32))

class Button(Window):
	_window_class_ = BUTTON
	_window_style_ = WS_CHILD | WS_VISIBLE | BS_DEFPUSHBUTTON

	def GetState(self):
		return self.SendMessage(BM_GETSTATE)

	def SetState(self, state = BST_FOCUS):
		self.SendMessage(BM_SETSTATE, state)

class RadioButton(Button):
	_window_class_ = BUTTON
	_window_style_ = WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_RADIOBUTTON

	def GetCheck(self):
		return self.SendMessage(BM_GETCHECK)

	def SetCheck(self, state = BST_UNCHECKED):
		self.SendMessage(BM_SETCHECK, state)

class AutoRadioButton(RadioButton):
	_window_class_ = BUTTON
	_window_style_ = WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_AUTORADIOBUTTON

class CheckBox(RadioButton):
	_window_class_ = BUTTON
	_window_style_ = WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_CHECKBOX

class AutoCheckBox(CheckBox):
	_window_class_ = BUTTON
	_window_style_ = WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_AUTOCHECKBOX

class StatusBar(Window):
	_window_class_ = STATUSCLASSNAME
	_window_style_ = WS_CHILD | WS_VISIBLE | SBS_SIZEGRIP

	def Simple(self, fSimple):
		self.SendMessage(SB_SIMPLE, fSimple, 0)

	def SetText(self, text = ''):
		txt = create_unicode_buffer(text)
		if not UNICODE:
			txt = create_string_buffer(text)
		#~ self.SendMessage(SB_SETTEXT, 255 | SBT_NOBORDERS, addressof(txt))
		self.SendMessage(SB_SETTEXT, 255 | SBT_NOBORDERS, txt)

class StaticText(Window):
	_window_class_ = WC_STATIC
	_window_style_ = WS_CHILD | WS_VISIBLE# | SS_SIMPLE
	_window_style_ex_ = 0

	def __init__(self, *args, **kwargs):
		Window.__init__(self, *args, **kwargs)

	def _GetText(self, returned_size = 0):
		text_length = GetWindowTextLength(self.handle) + 1
		text = c_wchar_p(' ' * text_length)
		if not UNICODE:
			text = c_char_p(' ' * text_length)
		returned_size = GetWindowText(self.handle, byref(text), text_length)
		return text.value

	def SetText(self, text = ''):
		return SetWindowText(self.handle, text)
		#~ txt = create_unicode_buffer(text)
		#~ if not UNICODE:
			#~ txt = create_string_buffer(text)
		#~ return self.SendMessage(WM_SETTEXT, 0, addressof(txt))

# Combo Box return Values
CB_OKAY             = 0
CB_ERR              = -1
CB_ERRSPACE         = -2
# Combo Box messages
CB_GETEDITSEL               = 0x0140
CB_LIMITTEXT                = 0x0141
CB_SETEDITSEL               = 0x0142
CB_ADDSTRING                = 0x0143
CB_DELETESTRING             = 0x0144
CB_DIR                      = 0x0145
CB_GETCOUNT                 = 0x0146
CB_GETCURSEL                = 0x0147
CB_GETLBTEXT                = 0x0148
CB_GETLBTEXTLEN             = 0x0149
CB_INSERTSTRING             = 0x014A
CB_RESETCONTENT             = 0x014B
CB_FINDSTRING               = 0x014C
CB_SELECTSTRING             = 0x014D
CB_SETCURSEL                = 0x014E
CB_SHOWDROPDOWN             = 0x014F
CB_GETITEMDATA              = 0x0150
CB_SETITEMDATA              = 0x0151
CB_GETDROPPEDCONTROLRECT    = 0x0152
CB_SETITEMHEIGHT            = 0x0153
CB_GETITEMHEIGHT            = 0x0154
CB_SETEXTENDEDUI            = 0x0155
CB_GETEXTENDEDUI            = 0x0156
CB_GETDROPPEDSTATE          = 0x0157
CB_FINDSTRINGEXACT          = 0x0158
CB_SETLOCALE                = 0x0159
CB_GETLOCALE                = 0x015A
if WINVER >= 0x0400:
	CB_GETTOPINDEX              = 0x015b
	CB_SETTOPINDEX              = 0x015c
	CB_GETHORIZONTALEXTENT      = 0x015d
	CB_SETHORIZONTALEXTENT      = 0x015e
	CB_GETDROPPEDWIDTH          = 0x015f
	CB_SETDROPPEDWIDTH          = 0x0160
	CB_INITSTORAGE              = 0x0161
if WINVER >= 0x0501:
	CB_GETCOMBOBOXINFO          = 0x0164
if WINVER >= 0x0501:
	CB_MSGMAX                   = 0x0165
elif WINVER >= 0x0400:
	CB_MSGMAX                   = 0x0162
else:
	CB_MSGMAX                   = 0x015B
#elif _WIN32_WCE >= 0x0400:
#	CB_MSGMAX                   = 0x0163
#if _WIN32_WCE >= 0x0400:
#	CB_MULTIPLEADDSTRING        = 0x0163

# Combo Box styles
CBS_SIMPLE            = 0x0001L
CBS_DROPDOWN          = 0x0002L
CBS_DROPDOWNLIST      = 0x0003L
CBS_OWNERDRAWFIXED    = 0x0010L
CBS_OWNERDRAWVARIABLE = 0x0020L
CBS_AUTOHSCROLL       = 0x0040L
CBS_OEMCONVERT        = 0x0080L
CBS_SORT              = 0x0100L
CBS_HASSTRINGS        = 0x0200L
CBS_NOINTEGRALHEIGHT  = 0x0400L
CBS_DISABLENOSCROLL   = 0x0800L
if WINVER >= 0x0400:
	CBS_UPPERCASE         = 0x2000L
	CBS_LOWERCASE         = 0x4000L

class ComboBox(Window):
	_window_class_ = WC_COMBOBOX
	_window_style_ = WS_VISIBLE | WS_CHILD | WS_OVERLAPPED | WS_VSCROLL | WS_TABSTOP | CBS_DROPDOWNLIST

	def AddString(self, text = ''):
		'return index of item is added'
		txt = create_unicode_buffer(text)
		if not UNICODE:
			txt = create_string_buffer(text)
		return self.SendMessage(CB_ADDSTRING, 0, addressof(txt))

	def DeleteString(self, index = 0):
		self.SendMessage(CB_DELETESTRING, index)

	def GetCount(self):
		return self.SendMessage(CB_GETCOUNT)

	def GetCurrentSelection(self):
		return self.SendMessage(CB_GETCURSEL)

	def SetCurrentSelection(self, index = 0):
		self.SendMessage(CB_SETCURSEL, index)

class ComboBoxEx(ComboBox):
	_window_class_ = WC_COMBOBOXEX
	_window_style_ = WS_VISIBLE | WS_CHILD | CBS_DROPDOWN

class Edit(Window):
	_window_class_ = WC_EDIT
	_window_style_ = WS_VISIBLE | WS_CHILD

class ListBox(Window):
	_window_class_ = 'ListBox'
	_window_style_ = WS_VISIBLE | WS_CHILD

	def AddString(self, text):
		txt = create_unicode_buffer(text)
		if not UNICODE:
			txt = create_string_buffer(text)
		self.SendMessage(LB_ADDSTRING, 0, addressof(txt))

	def InsertString(self, idx, text):
		txt = create_unicode_buffer(text)
		if not UNICODE:
			txt = create_string_buffer(text)
		self.SendMessage(LB_INSERTSTRING, idx, addressof(txt))

	def DeleteString(self, idx):
		self.SendMessage(LB_DELETESTRING, idx)

	def ResetContent(self):
		self.SendMessage(LB_RESETCONTENT)

	def GetCount(self):
		return self.SendMessage(LB_GETCOUNT)

	def SetTopIndex(self, idx):
		self.SendMessage (LB_SETTOPINDEX, idx)

class ProgressBar(Window):
	_window_class_ = PROGRESS_CLASS
	_window_style_ = WS_VISIBLE | WS_CHILD

	def SetRange(self, nMinRange, nMaxRange):
		if nMinRange > 65535 or nMaxRange > 65535:
			return self.SendMessage(PBM_SETRANGE32, nMinRange, nMaxRange)
		else:
			return self.SendMessage(PBM_SETRANGE, 0, MAKELPARAM(nMinRange, nMaxRange))

	def GetRange(self, fWhichLimit): # True=get low, False=get high range
		return self.SendMessage(PBM_GETRANGE, fWhichLimit, 0)

	def SetPos(self, nNewPos):
		return self.SendMessage(PBM_SETPOS, nNewPos, 0)

	def GetPos(self):
		return self.SendMessage(PBM_GETPOS, 0, 0)

	def SetBarColor(self, clrBar):
		return self.SendMessage(PBM_SETBARCOLOR, 0, clrBar)

	def SetBkColor(self, clrBk):
		return self.SendMessage(PBM_SETBKCOLOR, 0, clrBk)

	def SetStep(self, nStepInc):
		return self.SendMessage(PBM_SETSTEP, nStepInc, 0)

	def StepIt(self):
		return self.SendMessage(PBM_STEPIT, 0, 0)

	def DeltaPos(self, nIncrement):
		return self.SendMessage(PBM_DELTAPOS, nIncrement, 0)

class TrackBar(Window):
	_window_class_ = TRACKBAR_CLASS
	_window_style_ = WS_VISIBLE | WS_CHILD | TBS_AUTOTICKS | TBS_TOOLTIPS
	_window_style_ex_ = 0

	def __init__(self, *args, **kwargs):
		Window.__init__(self, *args, **kwargs)

	def SetRange(self, nMinRange, nMaxRange):
		return self.SendMessage(TBM_SETRANGE, 0, MAKELPARAM(nMinRange, nMaxRange))

	def SetPageSize(self, nSize):
		return self.SendMessage(TBM_SETPAGESIZE, 0, nSize)

	def GetPageSize(self):
		return self.SendMessage(TBM_GETPAGESIZE, 0, 0)

	def SetLineSize(self, nSize):
		return self.SendMessage(TBM_SETLINESIZE, 0, nSize)

	def GetLineSize(self):
		return self.SendMessage(TBM_GETLINESIZE, 0, 0)

	def GetRangeMin(self):
		return self.SendMessage(TBM_GETRANGEMIN, 0, 0)

	def GetRangeMax(self):
		return self.SendMessage(TBM_GETRANGEMAX, 0, 0)

	def SetPos(self,lPosition, fRedraw=1):
		return self.SendMessage(TBM_SETPOS, fRedraw, lPosition)

	def GetPos(self):
		return self.SendMessage(TBM_GETPOS, 0, 0)

	def ClearSel(self, fRedraw=0):
		return self.SendMessage(TBM_CLEARSEL, fRedraw, 0)

	def SetTickFreq(self, wFreq):
		return self.SendMessage(TBM_SETTICFREQ, wFreq, 0)

	def SetBuddy(self, hwndBuddy, fLocation=0):
		return self.SendMessage(TBM_SETBUDDY, fLocation, hwndBuddy)

class TabControl(Window):
	_window_class_ = WC_TABCONTROL
	_window_style_ = WS_VISIBLE | WS_CHILD | TCS_MULTILINE

	def InsertItem(self, iItem, item):        
		return self.SendMessage(TCM_INSERTITEM, iItem, addressof(item))

	def GetItem(self, index, mask):
		item = TCITEM()
		item.mask = mask
		if self.SendMessage(TCM_GETITEM, index, addressof(item)):
			return item
		else:
			raise 'error'
		
	def AdjustRect(self, fLarger, rect):
		lprect = byref(rect)
		self.SendMessage(TCM_ADJUSTRECT, fLarger, lprect)

	def GetCurSel(self):
		return self.SendMessage(TCM_GETCURSEL)

	def SetCurSel(self, iItem):
		return self.SendMessage(TCM_SETCURSEL, iItem)

class TreeView(Window):
	_window_class_ = WC_TREEVIEW
	_window_style_ = WS_CHILD | WS_VISIBLE | WS_TABSTOP | TVS_HASBUTTONS|TVS_LINESATROOT|TVS_HASLINES
	_window_style_ex_ = 0

	def InsertItem(self, hParent, hInsertAfter, itemEx):
		insertStruct = TVINSERTSTRUCT()
		insertStruct.hParent = hParent
		insertStruct.hInsertAfter = hInsertAfter
		insertStruct.itemex = itemEx

		return self.SendMessage(TVM_INSERTITEM, 0, addressof(insertStruct))

	def GetItem(self, item):
		return self.SendMessage(TVM_GETITEM, 0, addressof(item))

	def SetImageList(self, imageList, iImage = TVSIL_NORMAL):
		return self.SendMessage(TVM_SETIMAGELIST, iImage, handle(imageList))

	def GetChildItem(self, hitem):
		"""gets the first child of item"""
		return self.SendMessage(TVM_GETNEXTITEM, TVGN_CHILD, hitem)

	def GetNextItem(self, hitem):
		"""gets the next sibling from item"""
		return self.SendMessage(TVM_GETNEXTITEM, TVGN_NEXT, hitem)

	def GetRootItem(self):
		"""returns the root item"""
		return self.SendMessage(TVM_GETNEXTITEM, TVGN_ROOT)

	def CollapseAndReset(self, hitem):
		self.SendMessage(TVM_EXPAND, TVE_COLLAPSE|TVE_COLLAPSERESET, hitem)

	def DeleteAllItems(self):
		return self.SendMessage(TVM_DELETEITEM)

	def IsExpanded(self, hitem):
		return self.SendMessage(TVM_GETITEMSTATE, hitem, TVIS_EXPANDED)

	def Expand(self, hitem):
		return self.SendMessage(TVM_EXPAND, TVE_EXPAND, hitem)

	def EnsureVisible(self, hitem):
		return self.SendMessage(TVM_ENSUREVISIBLE, 0, hitem)

	def SelectItem(self, hitem):
		return self.SendMessage(TVM_SELECTITEM, TVGN_CARET, hitem)

	def GetSelection(self):
		return self.SendMessage(TVM_GETNEXTITEM, TVGN_CARET)

class ListView(Window):
	_window_class_ = WC_LISTVIEW
	_window_style_ = WS_CHILD | WS_VISIBLE | LVS_REPORT 
	_window_style_ex_ = 0
	_listview_style_ex_ = 0

	def __init__(self, *args, **kwargs):
		Window.__init__(self, *args, **kwargs)
		self.SetExtendedListViewStyle(self._listview_style_ex_, self._listview_style_ex_)

	#~ def __len__(self):
		#~ return self.GetItemCount()

	def InsertColumn(self, iCol, lvcolumn):
		return self.SendMessage(LVM_INSERTCOLUMN, iCol, addressof(lvcolumn))

	def SetColumn(self, iCol, lvcolumn):
		return self.SendMessage(LVM_SETCOLUMN, iCol, addressof(lvcolumn))

	def SetColumnWidth(self, iCol, width):
		return self.SendMessage(LVM_SETCOLUMNWIDTH, iCol, width)

	def InsertItem(self, item):
		if item.iItem == -1:
			item.iItem = self.GetItemCount()
		return self.SendMessage(LVM_INSERTITEM, 0, addressof(item))

	def SetItem(self, item):
		return self.SendMessage(LVM_SETITEM, 0, addressof(item))

	def DeleteAllItems(self):
		return self.SendMessage(LVM_DELETEALLITEMS)

	def SetItemState(self, i, state, stateMask):
		item = LVITEM()
		item.iItem = i
		item.mask = LVIF_STATE
		item.state = state
		item.stateMask = stateMask
		return self.SendMessage(LVM_SETITEMSTATE, i, addressof(item))

	def GetItemState(self, i, stateMask):
		return self.SendMessage(LVM_GETITEMSTATE, i, stateMask)

	def GetItemCount(self):
		return self.SendMessage(LVM_GETITEMCOUNT)

	def GetItem(self, i):
		item = LVITEM()
		item.iItem = i
		item.mask = LVIF_TEXT | LVIF_STATE
		self.SendMessage(LVM_GETITEM, 0, addressof(item))
		return item

	def GetItemParam(self, i):
		item = LVITEM()
		item.iItem = i
		item.mask = LVIF_PARAM
		self.SendMessage(LVM_GETITEM, 0, addressof(item))
		return item.lParam

	def SetItemCount(self, cItems, dwFlags = 0):
		self.SendMessage(LVM_SETITEMCOUNT, cItems, dwFlags)

	def GetSelectedCount(self):
		return self.SendMessage(LVM_GETSELECTEDCOUNT)

	def SetExtendedListViewStyle(self, dwExMask, dwExStyle):
		return self.SendMessage(LVM_SETEXTENDEDLISTVIEWSTYLE, dwExMask, dwExStyle)

	def GetHotItem(self):
		return self.SendMessage(LVM_GETHOTITEM)

	def HitTest(self):
		pinfo = LVHITTESTINFO()
		result = self.SendMessage(LVM_HITTEST, 0, byref(pinfo))
		return result, pinfo

class ToolBar(Window):
	_window_class_ = TOOLBARCLASSNAME
	_window_style_ = WS_CHILD | WS_VISIBLE

	def __init__(self, *args, **kwargs):
		Window.__init__(self, *args, **kwargs)
		self.SendMessage(TB_BUTTONSTRUCTSIZE, sizeof(TBBUTTON), 0)

	def PressButton(self, idButton, fPress):
		return self.SendMessage(TB_PRESSBUTTON, idButton, fPress)

	def GetRect(self, idCtrl):
		rc = RECT()
		self.SendMessage(TB_GETRECT, idCtrl, addressof(rc))
		return rc

	def HitTest(self, pt):
		return self.SendMessage(TB_HITTEST, 0, addressof(pt))

	def SetHotItem(self, idButton):
		return self.SendMessage(TB_SETHOTITEM, idButton)

	def GetHotItem(self):
		return self.SendMessage(TB_GETHOTITEM)

	def InsertButton(self, iButton, tbButton):
		return self.SendMessage(TB_INSERTBUTTON, iButton, addressof(tbButton))

	def insert_button(self, id_command = 0, caption = '', id_button = 0, id_image = I_IMAGENONE, fs_state = TBSTATE_ENABLED, fs_style = TBSTYLE_BUTTON):
		button = TBBUTTON()
		button.idCommand = id_command
		button.iBitmap = id_image
		button.fsState = fs_state
		button.fsStyle = fs_style
		button.dwData = 0
		if caption:
			button.iString = self.AddString(id_button, caption)
		result = self.InsertButton(id_button, button)
		if caption:
			self.SetButtonCaption(id_button, caption)
		return result

	def SetImageList(self, imageList, iImage = 0):
		return self.SendMessage(TB_SETIMAGELIST, iImage, handle(imageList))

	def SetButtonInfo(self, id_button = 0, info = TBBUTTONINFO()):
		return self.SendMessage(TB_SETBUTTONINFO, id_button, addressof(info))

	def SetButtonCaption(self, id_button = 0, caption = ''):
		info = TBBUTTONINFO()
		info.cbSize = sizeof(TBBUTTONINFO)
		info.dwMask = TBIF_TEXT
		info.pszText = caption
		return self.SetButtonInfo(id_button, info)

	def SetButtonSize(self, dxButton, dyButton):
		return self.SendMessage(TB_SETBUTTONSIZE, 0, MAKELONG(dxButton, dyButton))

	def SetAutoSize(self):
		return self.SendMessage(TB_AUTOSIZE, 0, 0)

	def AddString(self, uid = 0, text = ''):
		size_buffer = len(text)
		if UNICODE:
			text = c_wchar_p(text)
		else:
			text = c_char_p(text)
		LoadString(hInstance, uid, text, size_buffer)
		return self.SendMessage(TB_ADDSTRING, 0, text)

	def AddBitmap(self, nButtons, lptbab = TBADDBITMAP()):
		return self.SendMessage(TB_ADDBITMAP, nButtons, addressof(lptbab))

	def add_bitmap(self, id_bitmap = 0, hInst = HINST_COMMCTRL, nButtons = 0):
		lptbab = TBADDBITMAP()
		lptbab.hInst = hInst
		lptbab.nID = id_bitmap
		return self.AddBitmap(nButtons, lptbab)

class Rebar(Window):
	_window_class_ = REBARCLASSNAME
	_window_style_ = WS_CHILDWINDOW|WS_VISIBLE|WS_CLIPSIBLINGS|WS_CLIPCHILDREN|WS_BORDER|\
					RBS_VARHEIGHT|RBS_BANDBORDERS|RBS_AUTOSIZE|RBS_DBLCLKTOGGLE|\
					RBS_REGISTERDROP|CCS_NODIVIDER|CCS_TOP|CCS_NOPARENTALIGN
	_window_style_ex_ = WS_EX_LEFT|WS_EX_LTRREADING|WS_EX_RIGHTSCROLLBAR|WS_EX_TOOLWINDOW

	def __init__(self, *args, **kwargs):
		Window.__init__(self, *args, **kwargs)

		rebarInfo = REBARINFO()
		rebarInfo.cbSize = sizeof(REBARINFO)
		rebarInfo.fMask = 0
		rebarInfo.himl = NULL
		self.SendMessage(RB_SETBARINFO, 0, addressof(rebarInfo))

class ImageList(WindowsObject):
	__dispose__ = ImageList_Destroy

	def __init__(self, cx, cy, flags, cInitial, cGrow):
		WindowsObject.__init__(self, ImageList_Create(cx, cy, flags, cInitial, cGrow))

	def AddMasked(self, bitmap, crMask):
		return ImageList_AddMasked(self.handle, handle(bitmap), crMask)

	def SetBkColor(self, clrRef):
		ImageList_SetBkColor(self.handle, clrRef)

	def AddIcon(self, hIcon):
		return ImageList_AddIcon(self.handle, hIcon)

	def AddIconsFromModule(self, moduleName, cx, cy, uFlags):
		hdll = GetModuleHandle(moduleName)
		i = 1
		#dont know how many icons there are in module, this loop
		#breaks if there are no more because then an exception is thrown:
		while 1:
			try:
				hIcon = LoadImage(hdll, i, IMAGE_ICON, cx, cy, uFlags)
				if hIcon:
					self.AddIcon(hIcon)
				else:
					break
			except:
				break
			i += 1
