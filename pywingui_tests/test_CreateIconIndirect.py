'''Maxim Kolosov (2013).
Custom Icon example based on pyWinGUI.
Original was from C++ MSDN CreateAlphaCursor example.'''

from sys import hexversion
from pywingui.gdi import *
from pywingui.wtl import *

def CreateAlphaIconOrCursor(dwWidth = 32, dwHeight = 32, return_type = True):
	size = dwWidth * dwHeight
	text = 'rgba'
	if UNICODE and hexversion < 0x03000000:
		text = u'rgba'

	bi = BITMAPV5HEADER()
	#ZeroMemory(bi, sizeof(BITMAPV5HEADER))
	bi.bV5Size = sizeof(BITMAPV5HEADER)
	bi.bV5Width = dwWidth
	bi.bV5Height = dwHeight
	bi.bV5Planes = 1
	bi.bV5BitCount = 32
	bi.bV5Compression = BI_BITFIELDS
	# The following mask specification specifies a supported 32 BPP alpha format for Windows XP.
	bi.bV5RedMask = 0x00FF0000
	bi.bV5GreenMask = 0x0000FF00
	bi.bV5BlueMask = 0x000000FF
	bi.bV5AlphaMask = 0xFF000000

	hdc = GetDC(None)

	# Create the DIB section with an alpha channel.
	lpBits = c_void_p()
	offset = addressof(lpBits)
	hBitmap = CreateDIBSection(hdc, cast(pointer(bi), PBITMAPINFO), DIB_RGB_COLORS, byref(lpBits), None, 0)
	#~ hBitmap = CreateDIBSection(hdc, cast(pointer(bi), PBITMAPINFO), DIB_RGB_COLORS, offset, 0, 0)

	hMemDC = CreateCompatibleDC(hdc)
	ReleaseDC(None, hdc)

	# Draw something on the DIB section.
	hOldBitmap = SelectObject(hMemDC, hBitmap)
	PatBlt(hMemDC, 0, 0, dwWidth, dwHeight, WHITENESS)
	SetTextColor(hMemDC, RGB(0, 0, 0))
	SetBkMode(hMemDC, TRANSPARENT)#OPAQUE
	TextOut(hMemDC, 0, 9, text, 4)
	SelectObject(hMemDC, hOldBitmap)
	DeleteDC(hMemDC)

	# Create an empty mask bitmap.
	hMonoBitmap = CreateBitmap(dwWidth, dwHeight, 1, 1, None)

	# Set the alpha values for each pixel in the hBitmap so that the complete hBitmap is semi-transparent.
	MessageBox(None, 'Set Alpha bits not worked.\nIf you know as, fix me.', 'WARNING', MB_OK | MB_ICONINFORMATION)
	sz = sizeof(c_ulong)
	lpdwPixel = (c_ulong * size).from_address(offset)
	for i in range(size):
		# ==== like C way, not worked ====
		#~ lpdwPixel[i] &= 0x00FFFFFF # Clear the alpha bits
		#~ lpdwPixel[i] |= 0x9F000000 # Set the alpha bits to 0x9F (semi-transparent)
		# ==== another way, also not worked, uncomment memmove and look error ====
		dw = lpdwPixel[i]
		dw &= 0x00FFFFFF # Clear the alpha bits
		dw |= 0x9F000000 # Set the alpha bits to 0x9F (semi-transparent)
		#~ print(hex(lpdwPixel[i]), hex(dw).upper(), sz)
		#~ memset(offset+i*sz, dw, sz)
		#~ memmove(offset+i*sz, addressof(c_ulong(dw)), sz)

	ii = ICONINFO()
	ii.fIcon = return_type # Change fIcon to 'False' to create an alpha cursor
	ii.xHotspot = 0
	ii.yHotspot = 0
	ii.hbmMask = hMonoBitmap
	ii.hbmColor = hBitmap

	# Create the alpha cursor with the alpha DIB section.
	hAlphaIcon = CreateIconIndirect(ii)

	DeleteObject(hBitmap)
	DeleteObject(hMonoBitmap)

	return hAlphaIcon

class MyWindow(Window):
	_window_title_ = 'CreateIconIndirect example, based on MSDN CreateAlphaCursor example'
	_window_background_ = GetStockObject(WHITE_BRUSH)
	_window_icon_ = _window_icon_sm_ = CreateAlphaIconOrCursor()

	def OnDestroy(self, event):
		self.application.Quit()

	msg_handler(WM_DESTROY)(OnDestroy)

def main():
	myWindow = MyWindow(rcPos = RECT(0, 0, 320, 240))
	application = Application()
	myWindow.application = application
	application.Run()

if __name__ == '__main__':
	if WINVER >= 0x0500:
		main()
	else:
		MessageBox(None, 'Your OS version is less than XP.\nFor run this example, OS must be XP or later.', 'WARNING', MB_OK | MB_ICONINFORMATION)
