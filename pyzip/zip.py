import ctypes

zip_module = ctypes.CDLL('zip.dll')
func_type = ctypes.CFUNCTYPE

CreateZipFile = func_type(ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_char_p)(('CreateZipFile', zip_module))
CreateZipData = func_type(ctypes.c_void_p, ctypes.c_uint, ctypes.c_char_p)(('CreateZipData', zip_module))
CreateZipStream = func_type(ctypes.c_void_p, ctypes.c_char_p)(('CreateZipData', zip_module))
ZipAddFile = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p)(('ZipAddFile', zip_module))
ZipAddData = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_char_p, ctypes.c_uint)(('ZipAddData', zip_module))
ZipAddStream = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_void_p)(('ZipAddStream', zip_module))
ZipAddStreamLength = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_uint)(('ZipAddStreamLength', zip_module))
ZipAddDirectory = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_wchar_p)(('ZipAddDirectory', zip_module))
ZipGetData = func_type(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)(('ZipGetData', zip_module))
ZipClose = func_type(ctypes.c_ulong, ctypes.c_void_p)(('ZipClose', zip_module))

class ZipFile:
	def __init__(self, *args, **kwargs):
		self.name = args[0]
		self.password = ''
		if len(args) > 1:
			self.password = args[1]
		self.zhandle = CreateZipFile(self.name, self.password)
	def write(self, filename, arcname = None):
		if not arcname:
			arcname = filename
		return ZipAddFile(self.zhandle, arcname, filename)
	def writestr(self, filename, data):
		return ZipAddData(self.zhandle, filename, data, len(data))
	def close(self):
		return ZipClose(self.zhandle)


if __name__ == "__main__":
	data1 = 'some small data string'
	data2 = 'some other small data string'
	zhandle = CreateZipFile('test.zip', 'password')
	ZipAddData(zhandle, 'myfile1.txt', data1, len(data1))
	ZipAddData(zhandle, 'myfile2.txt', data2, len(data2))
	ZipClose(zhandle)

	# ZipFile compatibility
	f = ZipFile('oop_test.zip', 'password')
	f.writestr('myfile1.txt', data1)
	#~ f.write('zip.py', 'zip_archived.py')
	f.write('zip.py')
	f.close()
