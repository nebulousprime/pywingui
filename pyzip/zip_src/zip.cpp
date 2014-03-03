#include "stdafx.h"
#include "zip.h"


//ZIP_API int nzip=0;

ZIP_API HZIP CreateZipFile(const TCHAR* file_name, const char* password){return CreateZip(file_name, password);}
ZIP_API HZIP CreateZipData(void* buffer, unsigned int length, const char* password){return CreateZip(buffer, length, password);}
ZIP_API HZIP CreateZipStream(HANDLE handle, const char* password){return CreateZipHandle(handle, password);}
ZIP_API ZRESULT ZipAddFile(HZIP zip_handle, const TCHAR* destination_file_name, const TCHAR* source_file_name){return ZipAdd(zip_handle, destination_file_name, source_file_name);}
ZIP_API ZRESULT ZipAddData(HZIP zip_handle, const TCHAR* destination_file_name, void* data, unsigned int length){return ZipAdd(zip_handle, destination_file_name, data, length);}
ZIP_API ZRESULT ZipAddStream(HZIP zip_handle, const TCHAR* destination_file_name, HANDLE handle){return ZipAddHandle(zip_handle, destination_file_name, handle);}
ZIP_API ZRESULT ZipAddStreamLength(HZIP zip_handle, const TCHAR* destination_file_name, HANDLE handle, unsigned int length){return ZipAddHandle(zip_handle, destination_file_name, handle, length);}
ZIP_API ZRESULT ZipAddDirectory(HZIP zip_handle, const TCHAR* destination_file_name){return ZipAddFolder(zip_handle, destination_file_name);}
ZIP_API ZRESULT ZipGetData(HZIP zip_handle, void **buffer, unsigned long* length){return ZipGetMemory(zip_handle, buffer, length);}
ZIP_API ZRESULT ZipClose(HZIP zip_handle){return CloseZip(zip_handle);}
//ZIP_API unsigned int ZipMessage(ZRESULT code, TCHAR *buffer, unsigned int length){return FormatZipMessage(code, buffer, length);}
