# gdiplusflat.py
# Copyright (c) 2012 Maxim Kolosov

GDIPVER = 0x0100

# enum Status
Status = 0
Ok = 0
GenericError = 1
InvalidParameter = 2
OutOfMemory = 3
ObjectBusy = 4
InsufficientBuffer = 5
NotImplemented = 6
Win32Error = 7
WrongState = 8
Aborted = 9
FileNotFound = 10
ValueOverflow = 11
AccessDenied = 12
UnknownImageFormat = 13
FontFamilyNotFound = 14
FontStyleNotFound = 15
NotTrueTypeFont = 16
UnsupportedGdiplusVersion = 17
GdiplusNotInitialized = 18
PropertyNotFound = 19
PropertyNotSupported = 20
if GDIPVER >= 0x0110:
    ProfileNotFound = 21

# enum Unit constants
Unit = 0
UnitWorld = 0# World coordinate (non-physical unit)
UnitDisplay = 1# Variable -- for PageTransform only
UnitPixel = 2# Each unit is one device pixel.
UnitPoint = 3# Each unit is a printer's point, or 1/72 inch.
UnitInch = 4# Each unit is 1 inch.
UnitDocument = 5# Each unit is 1/300 inch.
UnitMillimeter = 6# Each unit is 1 millimeter.

# enum GdiplusStartupParams
GdiplusStartupParams = 0
GdiplusStartupDefault = 0
GdiplusStartupNoSetRound = 1
GdiplusStartupSetPSValue = 2
GdiplusStartupTransparencyMask = 0xFF000000

AlphaShift  = 24
RedShift    = 16
GreenShift  = 8
BlueShift   = 0

AlphaMask = 0xff000000
RedMask   = 0x00ff0000
GreenMask = 0x0000ff00
BlueMask  = 0x000000ff

def MakeARGB(a, r, g, b):
	return c_ulong((b <<  BlueShift) | (g << GreenShift) | (r <<   RedShift) | (a << AlphaShift))

from ctypes import *

DebugEventProc = WINFUNCTYPE(None, c_int, c_char_p)
NotificationHookProc = WINFUNCTYPE(c_int, c_void_p)
NotificationUnhookProc = WINFUNCTYPE(None, c_void_p)

class GdiplusStartupInput(Structure):
	_fields_ = [('GdiplusVersion', c_uint),
	('DebugEventCallback', DebugEventProc),
	('SuppressBackgroundThread', c_bool),
	('SuppressExternalCodecs', c_bool)]
#~ startup_input = GdiplusStartupInput(1, None, False, False)

class GdiplusStartupOutput(Structure):
	_fields_ = [('NotificationHook', NotificationHookProc),
	('NotificationUnhook', NotificationUnhookProc)]

#extern "C" Status WINAPI GdiplusStartup(OUT ULONG_PTR *token, const GdiplusStartupInput *input, OUT GdiplusStartupOutput *output);
GdiplusStartup = WINFUNCTYPE(c_int, c_void_p, POINTER(GdiplusStartupInput), c_void_p)(('GdiplusStartup', windll.gdiplus))

#extern "C" VOID WINAPI GdiplusShutdown(ULONG_PTR token);
GdiplusShutdown = WINFUNCTYPE(None, c_void_p)(('GdiplusShutdown', windll.gdiplus))


# Pen APIs

#GpStatus WINGDIPAPI GdipCreatePen1(ARGB color, REAL width, GpUnit unit, GpPen **pen);
_GdipCreatePen1 = WINFUNCTYPE(c_int, c_ulong, c_float, c_int, c_void_p)(('GdipCreatePen1', windll.gdiplus))
def GdipCreatePen1(color = MakeARGB(255, 255, 255, 255), width = 1.0, unit = UnitWorld):
	pen = c_void_p()
	status = _GdipCreatePen1(color, width, unit, byref(pen))
	return status, pen

#GpStatus WINGDIPAPI GdipCreatePen2(GpBrush *brush, REAL width, GpUnit unit, GpPen **pen);
GdipCreatePen2 = WINFUNCTYPE(c_int, c_void_p, c_float, c_int, c_void_p)(('GdipCreatePen2', windll.gdiplus))


# Graphics APIs

#GpStatus WINGDIPAPI GdipFlush(GpGraphics *graphics, GpFlushIntention intention);
GdipFlush = WINFUNCTYPE(c_int, c_void_p, c_int)(('GdipFlush', windll.gdiplus))

#GpStatus WINGDIPAPI GdipCreateFromHDC(HDC hdc, GpGraphics **graphics);
_GdipCreateFromHDC = WINFUNCTYPE(c_int, c_void_p, c_void_p)(('GdipCreateFromHDC', windll.gdiplus))
def GdipCreateFromHDC(hdc):
	graphics = c_void_p()
	status = _GdipCreateFromHDC(hdc, byref(graphics))
	return status, graphics

#GpStatus WINGDIPAPI GdipCreateFromHDC2(HDC hdc, HANDLE hDevice, GpGraphics **graphics);
GdipCreateFromHDC2 = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)(('GdipCreateFromHDC2', windll.gdiplus))

#GpStatus WINGDIPAPI GdipCreateFromHWND(HWND hwnd, GpGraphics **graphics);
GdipCreateFromHWND = WINFUNCTYPE(c_int, c_void_p, c_void_p)(('GdipCreateFromHWND', windll.gdiplus))

#GpStatus WINGDIPAPI GdipCreateFromHWNDICM(HWND hwnd, GpGraphics **graphics);
GdipCreateFromHWNDICM = WINFUNCTYPE(c_int, c_void_p, c_void_p)(('GdipCreateFromHWNDICM', windll.gdiplus))

#GpStatus WINGDIPAPI GdipDeleteGraphics(GpGraphics *graphics);
GdipDeleteGraphics = WINFUNCTYPE(c_int, c_void_p)(('GdipDeleteGraphics', windll.gdiplus))

#GpStatus WINGDIPAPI GdipGetDC(GpGraphics* graphics, HDC * hdc);
GdipGetDC = WINFUNCTYPE(c_int, c_void_p, c_void_p)(('GdipGetDC', windll.gdiplus))

#GpStatus WINGDIPAPI GdipReleaseDC(GpGraphics* graphics, HDC hdc);
GdipReleaseDC = WINFUNCTYPE(c_int, c_void_p, c_void_p)(('GdipReleaseDC', windll.gdiplus))


#GpStatus WINGDIPAPI GdipDrawLine(GpGraphics *graphics, GpPen *pen, REAL x1, REAL y1, REAL x2, REAL y2);
GdipDrawLine = WINFUNCTYPE(c_int, c_void_p, c_void_p, c_float, c_float, c_float, c_float)(('GdipDrawLine', windll.gdiplus))
