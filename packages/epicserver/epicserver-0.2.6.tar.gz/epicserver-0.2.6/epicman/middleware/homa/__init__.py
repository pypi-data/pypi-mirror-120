#!/usr/bin/env python3
"""Implementation of the HOMA protocol that uses swtich side DSCP QoS to
reduce message latency"""

class DATA(): pass # send -> recv
class GRANT(): pass # recv -> send
class RESEND(): pass # recv -> send
class BUSY(): pass # send -> recv

IPTOS_DSCP_AF11 = 0x28
IPTOS_DSCP_AF12 = 0x30
IPTOS_DSCP_AF13 = 0x38
IPTOS_DSCP_AF21 = 0x48
IPTOS_DSCP_AF22 = 0x50
IPTOS_DSCP_AF23 = 0x58
IPTOS_DSCP_AF31 = 0x68
IPTOS_DSCP_AF32 = 0x70
IPTOS_DSCP_AF33 = 0x78
IPTOS_DSCP_AF41 = 0x88
IPTOS_DSCP_AF42 = 0x90
IPTOS_DSCP_AF43 = 0x98
IPTOS_DSCP_EF   = 0xb8

CLASS_0 = 0x00   # Lowest Priority
CLASS_1 = 1 << 5 # BW Assured
CLASS_2 = 2 << 5 # BW Assured
CLASS_3 = 3 << 5 # BW Assured
CLASS_4 = 4 << 5 # BW Assured
CLASS_5 = 5 << 5 # BW Assured
CLASS_6 = 6 << 5 # Priority Queued
CLASS_7 = 7 << 5 # Highest Priority, Priority Queued

PRIORITY_CLASS_0 = [(socket.SOL_IP, socket.IP_TOS, CLASS_0)]
PRIORITY_CLASS_1 = [(socket.SOL_IP, socket.IP_TOS, CLASS_1)]
PRIORITY_CLASS_2 = [(socket.SOL_IP, socket.IP_TOS, CLASS_2)]
PRIORITY_CLASS_3 = [(socket.SOL_IP, socket.IP_TOS, CLASS_3)]
PRIORITY_CLASS_4 = [(socket.SOL_IP, socket.IP_TOS, CLASS_4)]
PRIORITY_CLASS_5 = [(socket.SOL_IP, socket.IP_TOS, CLASS_5)]
PRIORITY_CLASS_6 = [(socket.SOL_IP, socket.IP_TOS, CLASS_6)]
PRIORITY_CLASS_7 = [(socket.SOL_IP, socket.IP_TOS, CLASS_7)]

DEFAULT_PRIORITY = PRIORITY_CLASS_0

NO_FLAGS = 0

DEFAULT_MTU = 1500
LARGE_MTU = 9000

is_multipacket = len(data) > DEFAULT_MTU


socket.setsockoption(socket.SOL_IP, socket.IP_RECVTOS, True)
socket.setsockoption(socket.SOL_IP, socket.IP_TOS, DEFAULT_PRIORITY)

$ PMTU implementation
socket.setsockoption(socket.SOL_IP, socket.IP_MTU_DISCOVER, socket.IP_PMTUDISC_DO)
send -> EMSGSIZE via IP_RECVERR
then 
socket.getsockoption(socket.SOL_IP, socket.IP_MTU)
to get observed MTU

# try multiple sockets vs per socket options
socket.sendmsg(b'data', DEFAULT_PRIORITY, NO_FLAGS, ('localhost', 3030)]


# man 7 ip for PMTU discovery
# * Piggy back off monitoring?
# * wont work for non monitored hosts

# need round trip latency and BDR calculations
# * we schedule BW slots for remotes to fill in
# * Need to take into account how out of date taht info may be for remote end
SCHEDULING_GRANULARITY = 0.1 # seconds


TIMEOUT = SCHEDULING_GRANULARITY * 4 # for multi packet setups
