# iptypes.py
# Copyright (c) 2012 Maxim Kolosov

from ctypes import *

MAX_ADAPTER_DESCRIPTION_LENGTH = 128 # arb.
MAX_ADAPTER_NAME_LENGTH        = 256 # arb.
MAX_ADAPTER_ADDRESS_LENGTH     = 8   # arb.
DEFAULT_MINIMUM_ENTITIES       = 32  # arb.
MAX_HOSTNAME_LEN               = 128 # arb.
MAX_DOMAIN_NAME_LEN            = 128 # arb.
MAX_SCOPE_ID_LEN               = 256 # arb.
MAX_DHCPV6_DUID_LENGTH         = 130 # RFC 3315.

# Node Type
BROADCAST_NODETYPE             = 1
PEER_TO_PEER_NODETYPE          = 2
MIXED_NODETYPE                 = 4
HYBRID_NODETYPE                = 8

# Bit values of IP_ADAPTER_UNICAST_ADDRESS Flags field.
IP_ADAPTER_ADDRESS_DNS_ELIGIBLE = 0x01
IP_ADAPTER_ADDRESS_TRANSIENT    = 0x02

# Bit values of IP_ADAPTER_ADDRESSES Flags field.
IP_ADAPTER_DDNS_ENABLED               = 0x00000001
IP_ADAPTER_REGISTER_ADAPTER_SUFFIX    = 0x00000002
IP_ADAPTER_DHCP_ENABLED               = 0x00000004
IP_ADAPTER_RECEIVE_ONLY               = 0x00000008
IP_ADAPTER_NO_MULTICAST               = 0x00000010
IP_ADAPTER_IPV6_OTHER_STATEFUL_CONFIG = 0x00000020
IP_ADAPTER_NETBIOS_OVER_TCPIP_ENABLED = 0x00000040
IP_ADAPTER_IPV4_ENABLED               = 0x00000080
IP_ADAPTER_IPV6_ENABLED               = 0x00000100

# Flags used as argument to GetAdaptersAddresses().
# "SKIP" flags are added when the default is to include the information.
# "INCLUDE" flags are added when the default is to skip the information.
GAA_FLAG_SKIP_UNICAST                = 0x0001
GAA_FLAG_SKIP_ANYCAST                = 0x0002
GAA_FLAG_SKIP_MULTICAST              = 0x0004
GAA_FLAG_SKIP_DNS_SERVER             = 0x0008
GAA_FLAG_INCLUDE_PREFIX              = 0x0010
GAA_FLAG_SKIP_FRIENDLY_NAME          = 0x0020
GAA_FLAG_INCLUDE_WINS_INFO           = 0x0040
GAA_FLAG_INCLUDE_GATEWAYS            = 0x0080
GAA_FLAG_INCLUDE_ALL_INTERFACES      = 0x0100
GAA_FLAG_INCLUDE_ALL_COMPARTMENTS    = 0x0200
GAA_FLAG_INCLUDE_TUNNEL_BINDINGORDER = 0x0400


class IP_ADDRESS_STRING(Structure):
	_fields_ = [('String', c_char * 16)]
PIP_ADDRESS_STRING = POINTER(IP_ADDRESS_STRING)
IP_MASK_STRING = IP_ADDRESS_STRING
PIP_MASK_STRING = POINTER(IP_MASK_STRING)

class IP_ADDR_STRING(Structure):
	pass
PIP_ADDR_STRING = POINTER(IP_ADDR_STRING)
IP_ADDR_STRING._fields_ = [('Next', PIP_ADDR_STRING),
	('IpAddress', IP_ADDRESS_STRING),
	('IpMask', IP_MASK_STRING),
	('Context', c_ulong)]

# ADAPTER_INFO - per-adapter information. All IP addresses are stored as strings
class IP_ADAPTER_INFO(Structure):
	pass
PIP_ADAPTER_INFO = POINTER(IP_ADAPTER_INFO)
IP_ADAPTER_INFO._fields_ = [('Next', PIP_ADAPTER_INFO),
	('ComboIndex', c_ulong),
	('AdapterName', c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
	('Description', c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
	('AddressLength', c_uint),
	('Address', c_byte * MAX_ADAPTER_ADDRESS_LENGTH),
	('Index', c_ulong),
	('Type', c_uint),
	('DhcpEnabled', c_uint),
	('CurrentIpAddress', PIP_ADDR_STRING),
	('IpAddressList', IP_ADDR_STRING),
	('GatewayList', IP_ADDR_STRING),
	('DhcpServer', IP_ADDR_STRING),
	('HaveWins', c_bool),
	('PrimaryWinsServer', IP_ADDR_STRING),
	('SecondaryWinsServer', IP_ADDR_STRING),
	('LeaseObtained', c_int64),
	('LeaseExpires', c_int64)]

class FIXED_INFO(Structure):
	_fields_ = [('HostName', c_char * (MAX_HOSTNAME_LEN + 4)),
	('DomainName', c_char * (MAX_DOMAIN_NAME_LEN + 4)),
	('CurrentDnsServer', PIP_ADDR_STRING),
	('DnsServerList', IP_ADDR_STRING),
	('NodeType', c_uint),
	('ScopeId', c_char * (MAX_SCOPE_ID_LEN + 4)),
	('EnableRouting', c_uint),
	('EnableProxy', c_uint),
	('EnableDns', c_uint)]
