#ifdef ZIP_EXPORTS
#define ZIP_API __declspec(dllexport)
#else
#define ZIP_API __declspec(dllimport)
#endif

#include "zip_utils.h"


#ifdef __cplusplus
extern "C" {
#endif

ZIP_API HZIP CreateZipFile(const TCHAR* file_name, const char* password);
ZIP_API HZIP CreateZipData(void* buffer, unsigned int length, const char* password);
ZIP_API HZIP CreateZipStream(HANDLE handle, const char* password);
ZIP_API ZRESULT ZipAddFile(HZIP zip_handle, const TCHAR* destination_file_name, const TCHAR* source_file_name);
ZIP_API ZRESULT ZipAddData(HZIP zip_handle, const TCHAR* destination_file_name, void* data, unsigned int length);
ZIP_API ZRESULT ZipAddStream(HZIP zip_handle, const TCHAR* destination_file_name, HANDLE handle);
ZIP_API ZRESULT ZipAddStreamLength(HZIP zip_handle, const TCHAR* destination_file_name, HANDLE handle, unsigned int length);
ZIP_API ZRESULT ZipAddDirectory(HZIP zip_handle, const TCHAR* destination_file_name);
ZIP_API ZRESULT ZipGetData(HZIP zip_handle, void **buffer, unsigned long* length);
ZIP_API ZRESULT ZipClose(HZIP zip_handle);
//ZIP_API unsigned int ZipMessage(ZRESULT code, TCHAR *buffer, unsigned int length);

#ifdef __cplusplus
}
#endif
