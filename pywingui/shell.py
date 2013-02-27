from windows import *
from sdkddkver import _WIN32_IE

NIN_SELECT          = (WM_USER + 0)
NINF_KEY            = 0x1
NIN_KEYSELECT       = (NIN_SELECT | NINF_KEY)

NIN_BALLOONSHOW     = (WM_USER + 2)
NIN_BALLOONHIDE     = (WM_USER + 3)
NIN_BALLOONTIMEOUT  = (WM_USER + 4)
NIN_BALLOONUSERCLICK = (WM_USER + 5)


NIM_ADD        = 0x00000000
NIM_MODIFY     = 0x00000001
NIM_DELETE     = 0x00000002
NIM_SETFOCUS   = 0x00000003
NIM_SETVERSION = 0x00000004


NIF_MESSAGE    = 0x00000001
NIF_ICON       = 0x00000002
NIF_TIP        = 0x00000004
NIF_STATE      = 0x00000008
NIF_INFO       = 0x00000010
NIF_GUID       = 0x00000020

NIS_HIDDEN            =  0x00000001
NIS_SHAREDICON        =  0x00000002

NIIF_NONE      = 0x00000000
NIIF_INFO      = 0x00000001
NIIF_WARNING   = 0x00000002
NIIF_ERROR     = 0x00000003
NIIF_ICON_MASK = 0x0000000F
NIIF_NOSOUND   = 0x00000010

NOTIFYICON_VERSION = 3

CSIDL_LOCAL_APPDATA = 0x001c

SHGFP_TYPE_CURRENT  = 0
SHGFP_TYPE_DEFAULT  = 1

# simple analog of original comtypes GUID class
class GUID(Structure):
	_fields_ = [('Data1', DWORD),
	('Data2', WORD),
	('Data3', WORD),
	('Data4', BYTE * 8)]

class NOTIFYICONDATA(Structure):
	_fields_ = [('cbSize', DWORD),
	('hWnd', HWND),
	('uID', UINT),
	('uFlags', UINT),
	('uCallbackMessage', UINT),
	('hIcon', HICON),
	('szTip', TCHAR * 64),
	('dwState', DWORD),
	('dwStateMask', DWORD),
	('szInfo', TCHAR * 256),
	('uVersion', UINT), #todo really a union
	('szInfoTitle', TCHAR * 64),
	('dwInfoFlags', DWORD),
	('guidItem', GUID)]

# Platform IDs for DLLVERSIONINFO
DLLVER_PLATFORM_WINDOWS = 0x00000001# Windows 95
DLLVER_PLATFORM_NT      = 0x00000002# Windows NT
class DLLVERSIONINFO(Structure):
	_fields_ = [('cbSize', c_ulong),
	('dwMajorVersion', c_ulong),
	('dwMinorVersion', c_ulong),
	('dwBuildNumber', c_ulong),
	('dwPlatformID', c_ulong)]
LPDLLVERSIONINFO = POINTER(DLLVERSIONINFO)

if _WIN32_IE >= 0x0501:
	class DLLVERSIONINFO2(Structure):
		'ullVersion field encoded as: Major 0xFFFF 0000 0000 0000; Minor 0x0000 FFFF 0000 0000; Build 0x0000 0000 FFFF 0000; QFE 0x0000 0000 0000 FFFF'
		_fields_ = [('info1', LPDLLVERSIONINFO),
		('dwFlags', c_ulong),
		('ullVersion', c_ulonglong)]
	DLLVER_MAJOR_MASK = 0xFFFF000000000000
	DLLVER_MINOR_MASK = 0x0000FFFF00000000
	DLLVER_BUILD_MASK = 0x00000000FFFF0000
	DLLVER_QFE_MASK   = 0x000000000000FFFF

Shell_NotifyIcon = windll.shell32.Shell_NotifyIcon
SHGetFolderPath = windll.shell32.SHGetFolderPathA

#~ SHSTDAPI_(UINT) ExtractIconExA(LPCSTR lpszFile, int nIconIndex, __out_ecount_opt(nIcons) HICON *phiconLarge, __out_ecount_opt(nIcons) HICON *phiconSmall, UINT nIcons);
#~ SHSTDAPI_(UINT) ExtractIconExW(LPCWSTR lpszFile, int nIconIndex, __out_ecount_opt(nIcons) HICON *phiconLarge, __out_ecount_opt(nIcons) HICON *phiconSmall, UINT nIcons);

ExtractIcon = WINFUNCTYPE(c_void_p, c_void_p, c_wchar_p, c_uint)(('ExtractIconW', windll.shell32))
_ExtractIconEx = WINFUNCTYPE(c_uint, c_wchar_p, c_int, c_void_p, c_void_p, c_uint)(('ExtractIconExW', windll.shell32))
if not UNICODE:
	ExtractIcon = WINFUNCTYPE(c_void_p, c_void_p, c_char_p, c_uint)(('ExtractIconA', windll.shell32))
	_ExtractIconEx = WINFUNCTYPE(c_uint, c_char_p, c_int, c_void_p, c_void_p, c_uint)(('ExtractIconExA', windll.shell32))

def ExtractIconEx(lpszFile, nIconIndex = 0, nIcons = 1):
	phiconLarge = c_void_p()
	phiconSmall = c_void_p()
	result = _ExtractIconEx(lpszFile, nIconIndex, byref(phiconLarge), byref(phiconSmall), nIcons)
	return result, phiconLarge, phiconSmall

_DllGetVersion = WINFUNCTYPE(c_long, LPDLLVERSIONINFO)(('DllGetVersion', windll.shell32))
def DllGetVersion():
	info = DLLVERSIONINFO()
	info.cbSize = sizeof(DLLVERSIONINFO)
	result = _DllGetVersion(info)
	return result, info
