# iphlpapi.py
# Copyright (c) 2012 Maxim Kolosov

from ctypes import *

NET_ADDRESS_FORMAT_ = 0
NET_ADDRESS_FORMAT = 0
NET_ADDRESS_FORMAT_UNSPECIFIED = 0
NET_ADDRESS_DNS_NAME = 1
NET_ADDRESS_IPV4 = 2
NET_ADDRESS_IPV6 = 3

NET_STRING_IPV4_ADDRESS = 0x00000001
# The string identifies an IPv4 Host/router using literal address.
# (port or prefix not allowed) 
NET_STRING_IPV4_SERVICE = 0x00000002
# The string identifies an IPv4 service using literal address.
# (port required; prefix not allowed) 
NET_STRING_IPV4_NETWORK = 0x00000004
# The string identifies an IPv4 network.
# (prefix required; port not allowed) 
NET_STRING_IPV6_ADDRESS = 0x00000008
# The string identifies an IPv6 Host/router using literal address.
# (port or prefix not allowed; scope-id allowed) 
NET_STRING_IPV6_ADDRESS_NO_SCOPE = 0x00000010
# The string identifies an IPv6 Host/router using literal address
# where the interface context is already known.
# (port or prefix not allowed; scope-id not allowed) 
NET_STRING_IPV6_SERVICE = 0x00000020
# The string identifies an IPv6 service using literal address.
# (port required; prefix not allowed; scope-id allowed) 
NET_STRING_IPV6_SERVICE_NO_SCOPE = 0x00000040
# The string identifies an IPv6 service using literal address
# where the interface context is already known.
# (port required; prefix not allowed; scope-id not allowed) 
NET_STRING_IPV6_NETWORK = 0x00000080
# The string identifies an IPv6 network.
# (prefix required; port or scope-id not allowed) 
NET_STRING_NAMED_ADDRESS = 0x00000100
# The string identifies an Internet Host using DNS.
# (port or prefix or scope-id not allowed) 
NET_STRING_NAMED_SERVICE = 0x00000200
# The string identifies an Internet service using DNS.
# (port required; prefix or scope-id not allowed)

NET_STRING_IP_ADDRESS = NET_STRING_IPV4_ADDRESS | NET_STRING_IPV6_ADDRESS
NET_STRING_IP_ADDRESS_NO_SCOPE = NET_STRING_IPV4_ADDRESS | NET_STRING_IPV6_ADDRESS_NO_SCOPE
NET_STRING_IP_SERVICE = NET_STRING_IPV4_SERVICE | NET_STRING_IPV6_SERVICE
NET_STRING_IP_SERVICE_NO_SCOPE = NET_STRING_IPV4_SERVICE | NET_STRING_IPV6_SERVICE_NO_SCOPE
NET_STRING_IP_NETWORK = NET_STRING_IPV4_NETWORK | NET_STRING_IPV6_NETWORK
NET_STRING_ANY_ADDRESS = NET_STRING_NAMED_ADDRESS | NET_STRING_IP_ADDRESS
NET_STRING_ANY_ADDRESS_NO_SCOPE = NET_STRING_NAMED_ADDRESS | NET_STRING_IP_ADDRESS_NO_SCOPE
NET_STRING_ANY_SERVICE = NET_STRING_NAMED_SERVICE | NET_STRING_IP_SERVICE
NET_STRING_ANY_SERVICE_NO_SCOPE = NET_STRING_NAMED_SERVICE | NET_STRING_IP_SERVICE_NO_SCOPE

from pywingui.sdkddkver import NTDDI_VERSION, NTDDI_WIN2K, NTDDI_LONGHORN
from ipifcons import *
from iptypes import *
from ifmib import *
from ipmib import *
from tcpmib import *
from udpmib import *

_GetNumberOfInterfaces = WINFUNCTYPE(c_ulong, c_void_p)(('GetNumberOfInterfaces', windll.iphlpapi))
def GetNumberOfInterfaces():
	'Retrieves the number of interfaces in the system. These include LAN and WAN interfaces'
	result2 = c_ulong()
	result1 = _GetNumberOfInterfaces(byref(result2))
	return result1, result2

_GetIfEntry = WINFUNCTYPE(c_ulong, c_void_p)(('GetIfEntry', windll.iphlpapi))
def GetIfEntry(pIfRow = None):
	'Gets the MIB-II ifEntry. The dwIndex field of the MIB_IFROW should be set to the index of the interface being queried'
	if not pIfRow:
		pIfRow = PMIB_IFROW()
	return _GetIfEntry(pIfRow)

_GetIfTable = WINFUNCTYPE(c_ulong, PMIB_IFTABLE, c_void_p, c_bool)(('GetIfTable', windll.iphlpapi))
def GetIfTable(pdwSize = None, bOrder = True):
	'Gets the MIB-II IfTable'
	pIfTable = PMIB_IFTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetIfTable(pIfTable, byref(pdwSize), bOrder)
	return result, pIfTable

_GetIpAddrTable = WINFUNCTYPE(c_ulong, PMIB_IPADDRTABLE, c_void_p, c_bool)(('GetIpAddrTable', windll.iphlpapi))
def GetIpAddrTable(pdwSize = None, bOrder = True):
	'Gets the Interface to IP Address mapping'
	pIpAddrTable = PMIB_IPADDRTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetIpAddrTable(pIpAddrTable, byref(pdwSize), bOrder)
	return result, pIpAddrTable

_GetIpNetTable = WINFUNCTYPE(c_ulong, PMIB_IPNETTABLE, c_void_p, c_bool)(('GetIpNetTable', windll.iphlpapi))
def GetIpNetTable(pdwSize = None, bOrder = True):
	'Gets the current IP Address to Physical Address (ARP) mapping'
	IpNetTable = PMIB_IPNETTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetIpNetTable(IpNetTable, byref(pdwSize), bOrder)
	return result, IpNetTable

_GetIpForwardTable = WINFUNCTYPE(c_ulong, PMIB_IPFORWARDTABLE, c_void_p, c_bool)(('GetIpForwardTable', windll.iphlpapi))
def GetIpForwardTable(pdwSize = None, bOrder = True):
	'Gets the IP Routing Table  (RFX XXXX)'
	pIpForwardTable = PMIB_IPFORWARDTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetIpForwardTable(pIpForwardTable, byref(pdwSize), bOrder)
	return result, pIpForwardTable


# Gets TCP Connection/UDP Listener Table

_GetTcpTable = WINFUNCTYPE(c_ulong, PMIB_TCPTABLE, c_void_p, c_bool)(('GetTcpTable', windll.iphlpapi))
def GetTcpTable(pdwSize = None, bOrder = True):
	'Gets the TCP Connection Table'
	TcpTable = PMIB_TCPTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetTcpTable(TcpTable, byref(pdwSize), bOrder)
	return result, TcpTable

_GetExtendedTcpTable = WINFUNCTYPE(c_ulong, c_void_p, c_void_p, c_bool, c_ulong, c_int, c_ulong)(('GetExtendedTcpTable', windll.iphlpapi))
def GetExtendedTcpTable(pTcpTable = None, pdwSize = None, bOrder = True, ulAf = 0, TableClass = 0, Reserved = 0):
	if not pTcpTable:
		pTcpTable = c_void_p()
	if not pdwSize:
		pdwSize = c_ulong()
	return _GetExtendedTcpTable(byref(pTcpTable), byref(pdwSize), bOrder, ulAf, TableClass, Reserved)

_GetOwnerModuleFromTcpEntry = WINFUNCTYPE(c_ulong, PMIB_TCPROW_OWNER_MODULE, c_int, c_void_p, c_void_p)(('GetOwnerModuleFromTcpEntry', windll.iphlpapi))
def GetOwnerModuleFromTcpEntry(pTcpEntry = PMIB_TCPROW_OWNER_MODULE(), Class = 0, pBuffer = None, pdwSize = None):
	if not pBuffer:
		pBuffer = c_void_p()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetOwnerModuleFromTcpEntry(pTcpEntry, Class, byref(pBuffer), byref(pdwSize))
	return result, pBuffer

_GetUdpTable = WINFUNCTYPE(c_ulong, PMIB_UDPTABLE, c_void_p, c_bool)(('GetUdpTable', windll.iphlpapi))
def GetUdpTable(pdwSize = None, bOrder = True):
	'Gets the UDP Listener Table'
	UdpTable = PMIB_UDPTABLE()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetUdpTable(UdpTable, byref(pdwSize), bOrder)
	return result, UdpTable

_GetExtendedUdpTable = WINFUNCTYPE(c_ulong, c_void_p, c_void_p, c_bool, c_ulong, c_int, c_ulong)(('GetExtendedUdpTable', windll.iphlpapi))
def GetExtendedUdpTable(pUdpTable = None, pdwSize = None, bOrder = True, ulAf = 0, TableClass = 0, Reserved = 0):
	if not pUdpTable:
		pUdpTable = c_void_p()
	if not pdwSize:
		pdwSize = c_ulong()
	return _GetExtendedUdpTable(byref(pUdpTable), byref(pdwSize), bOrder, ulAf, TableClass, Reserved)

_GetOwnerModuleFromUdpEntry = WINFUNCTYPE(c_ulong, PMIB_UDPROW_OWNER_MODULE, c_int, c_void_p, c_void_p)(('GetOwnerModuleFromUdpEntry', windll.iphlpapi))
def GetOwnerModuleFromUdpEntry(pUdpEntry = PMIB_UDPROW_OWNER_MODULE(), Class = 0, pBuffer = None, pdwSize = None):
	if not pBuffer:
		pBuffer = c_void_p()
	if not pdwSize:
		pdwSize = c_ulong()
	result = _GetOwnerModuleFromUdpEntry(pUdpEntry, Class, byref(pBuffer), byref(pdwSize))
	return result, pBuffer

if NTDDI_VERSION >= NTDDI_LONGHORN:
	_GetTcpTable2 = WINFUNCTYPE(c_ulong, PMIB_TCPTABLE2, c_void_p, c_bool)(('GetTcpTable2', windll.iphlpapi))
	def GetTcpTable2(pdwSize = None, bOrder = True):
		TcpTable = PMIB_TCPTABLE2()
		if not pdwSize:
			pdwSize = c_ulong()
		result = _GetTcpTable2(TcpTable, byref(pdwSize), bOrder)
		return result, TcpTable


# Deprecated APIs, Added for documentation.
if NTDDI_VERSION < NTDDI_LONGHORN:
	_AllocateAndGetTcpExTableFromStack = WINFUNCTYPE(c_ulong, POINTER(c_void_p), c_bool, c_ulong, c_ulong, c_ulong)(('AllocateAndGetTcpExTableFromStack', windll.iphlpapi))
	def AllocateAndGetTcpExTableFromStack(ppTcpTable = None, bOrder = True, hHeap = 0, dwFlags = 0, dwFamily = 0):
		if not ppTcpTable:
			ppTcpTable = pointer(c_void_p())
		return _AllocateAndGetTcpExTableFromStack(ppTcpTable, bOrder, hHeap, dwFlags, dwFamily)
	_AllocateAndGetUdpExTableFromStack = WINFUNCTYPE(c_ulong, POINTER(c_void_p), c_bool, c_ulong, c_ulong, c_ulong)(('AllocateAndGetUdpExTableFromStack', windll.iphlpapi))
	def AllocateAndGetUdpExTableFromStack(ppUdpTable = None, bOrder = True, hHeap = 0, dwFlags = 0, dwFamily = 0):
		if not ppUdpTable:
			ppUdpTable = pointer(c_void_p())
		return _AllocateAndGetUdpExTableFromStack(ppUdpTable, bOrder, hHeap, dwFlags, dwFamily)

# The following definitions require Winsock2.
# Minimum supported client Windows Vista 
# Minimum supported server Windows Server 2008 
if NTDDI_VERSION >= NTDDI_LONGHORN:

	_GetTcp6Table = WINFUNCTYPE(c_ulong, PMIB_TCP6TABLE, c_void_p, c_bool)(('GetTcp6Table', windll.iphlpapi))
	def GetTcp6Table(pdwSize = None, bOrder = True):
		Tcp6Table = PMIB_TCP6TABLE()
		if not pdwSize:
			pdwSize = c_ulong()
		result = _GetTcp6Table(Tcp6Table, byref(pdwSize), bOrder)
		return result, Tcp6Table

	_GetTcp6Table2 = WINFUNCTYPE(c_ulong, PMIB_TCP6TABLE2, c_void_p, c_bool)(('GetTcp6Table2', windll.iphlpapi))
	def GetTcp6Table2(pdwSize = None, bOrder = True):
		Tcp6Table2 = PMIB_TCP6TABLE2()
		if not pdwSize:
			pdwSize = c_ulong()
		result = _GetTcp6Table2(Tcp6Table2, byref(pdwSize), bOrder)
		return result, Tcp6Table2

	GetPerTcpConnectionEStats = WINFUNCTYPE(c_ulong, PMIB_TCPROW, c_int, c_void_p, c_ulong, c_ulong, c_void_p, c_ulong, c_ulong, c_void_p, c_ulong, c_ulong)(('GetPerTcpConnectionEStats', windll.iphlpapi))
	SetPerTcpConnectionEStats = WINFUNCTYPE(c_ulong, PMIB_TCPROW, c_int, c_void_p, c_ulong, c_ulong, c_ulong)(('SetPerTcpConnectionEStats', windll.iphlpapi))

	#if _WS2IPDEF_:
	GetPerTcp6ConnectionEStats = WINFUNCTYPE(c_ulong, PMIB_TCP6ROW, c_int, c_void_p, c_ulong, c_ulong, c_void_p, c_ulong, c_ulong, c_void_p, c_ulong, c_ulong)(('GetPerTcp6ConnectionEStats', windll.iphlpapi))
	SetPerTcp6ConnectionEStats = WINFUNCTYPE(c_ulong, PMIB_TCP6ROW, c_int, c_void_p, c_ulong, c_ulong, c_ulong)(('SetPerTcp6ConnectionEStats', windll.iphlpapi))

	GetOwnerModuleFromTcp6Entry = WINFUNCTYPE(c_ulong, PMIB_TCP6ROW_OWNER_MODULE, c_int, c_void_p, c_void_p)(('GetOwnerModuleFromTcp6Entry', windll.iphlpapi))

	_GetUdp6Table = WINFUNCTYPE(c_ulong, PMIB_UDP6TABLE, c_void_p, c_bool)(('GetUdp6Table', windll.iphlpapi))
	def GetUdp6Table(pdwSize = None, bOrder = True):
		Udp6Table = PMIB_UDP6TABLE()
		if not pdwSize:
			pdwSize = c_ulong()
		result = _GetUdp6Table(Udp6Table, byref(pdwSize), bOrder)
		return result, Udp6Table

	GetOwnerModuleFromUdp6Entry = WINFUNCTYPE(c_ulong, PMIB_UDP6ROW_OWNER_MODULE, c_int, c_void_p, c_void_p)(('GetOwnerModuleFromUdp6Entry', windll.iphlpapi))
	#end if _WS2IPDEF_

	GetOwnerModuleFromPidAndInfo = WINFUNCTYPE(c_ulong, c_ulong, c_void_p, c_int, c_void_p, c_void_p)(('GetOwnerModuleFromPidAndInfo', windll.iphlpapi))


# Gets IP/ICMP/TCP/UDP Statistics

if NTDDI_VERSION >= NTDDI_WIN2K:

	_GetIpStatistics = WINFUNCTYPE(c_ulong, PMIB_IPSTATS)(('GetIpStatistics', windll.iphlpapi))
	def GetIpStatistics():
		'retrieves the IP statistics for the current computer'
		Statistics = MIB_IPSTATS()
		#~ Statistics = cast(cdll.msvcrt.malloc(sizeof(MIB_IPSTATS)), PMIB_IPSTATS)
		result = _GetIpStatistics(Statistics)
		return result, Statistics


if __name__ == '__main__':
	if NTDDI_VERSION >= NTDDI_WIN2K:
		from pywingui.error import NO_ERROR
		dwRetval, pStats = GetIpStatistics()
		if dwRetval != NO_ERROR:
			print('GetIpStatistics call failed with %d' % dwRetval)
		else:
			print(repr(pStats))
		#~ cdll.msvcrt.free(pStats)
	else:
		print('OS version is not enough for GetIpStatistics function')
