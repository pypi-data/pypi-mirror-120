#!/bin/bash

set -e -u

function help() {
    echo "Script to simulate various network conditions"
    echo "  $0 [NAME] [CMD] [ARGS]"
    echo ""
    echo "Link quality settings are provided via envionment variables:"
    echo "  LATENCY: The ammount to delay packets by"
    echo "  JITTER: The ammount to vary the pacekt delay by, varies above AND below"
    echo "          the value from LATENCY (ie LATENCY=10ms JITTER=5ms will cause"
    echo "          packet delays between 5ms to 15ms"
    echo "  RATE: The bandwidth of the link to simulate"
    echo "  PACKETDROP: Random % of packets to be dropped, use 0% for a local ethernet link"
    echo ""
    echo "Example Output:"
    cat << EOF
sudo LATENCY=20mS JITTER=10ms RATE=1Mbit PACKET_DROP=4% ./simulate-network.sh testing sleep 10000
Created container: testing
Remote IP: 172.16.3.2
Latency: 20mS, 10ms jitter
Bandwidth: 1Mbit
Packet Drop: 4%
Executing command: sleep 10000
EOF
    echo ""
    echo "** NOTE: Must be run as root **"
    echo "This script still clean up after itself on all catchable errors"
    echo "Kill -9 may require deleting the netns and upstream interface"
    echo "see cleanup_netns() for the commands to run"
}

if [ "$#" -lt 2 ]; then
    help > /dev/stderr
    exit 1
fi

if [ "$(id -u)" != "0" ]; then
    echo "This script needs to be run as root" > /dev/stderr
    exit 1
fi

NETNS="$1"
shift 1
CMD="$@"

LATENCY=${LATENCY:-"100ms"}
JITTER=${JITTER:-"3ms"}
RATE=${RATE:-"100kbit"}
PACKET_DROP=${PACKET_DROP:-"3%"}
HOST_IF=${HOST_IF:-'epic-host'}
HOST_IP=${HOST_IP:-'172.16.3.1'}
NETNS_IF=${NETNS_IF:-'epic-netns'}
NETNS_IP=${NETNS_IP:-'172.16.3.2'}

function cleanup_netns() {
    # we are using set -e and need to guard these 
    # statments to ensure they execute
    ip netns delete "$1" || true
    ip li del "$2" || true
}

function create_netns() {
    ip netns add "$1"
}

function create_link() {
    ip li add $1 type veth peer name $3
    ip ad add ${2}/30 dev $1
    ip li set $1 up
}

function qos_link() {
    tc qdisc add dev $1 root netem delay $3 $4 loss random $5 rate $6
    tc qdisc add dev $2 root netem delay $3 $4 loss random $5 rate $6
}

function link_in_netns() {
    ip li set $2 netns $1
    ip netns exec $1 ip ad add ${3}/30 dev $2
    ip netns exec $1 ip li set $2 up
}

function exec_cmd_in_netns() {
    NETNS=$1
    shift 1
    ip netns exec $NETNS "$@"
}



# Ensure resources are cleaned up
trap "cleanup_netns $NETNS $HOST_IF" SIGTERM EXIT

create_netns "$NETNS"
create_link "$HOST_IF" "$HOST_IP" "$NETNS_IF"
qos_link "$HOST_IF" "$NETNS_IF" "$LATENCY" "$JITTER" "$PACKET_DROP" "$RATE"
link_in_netns "$NETNS" "$NETNS_IF" "$NETNS_IP"

echo "Created container: $NETNS"
echo "Remote IP: $NETNS_IP"
echo "Latency: $LATENCY, $JITTER jitter"
echo "Bandwidth: $RATE"
echo "Packet Drop: $PACKET_DROP"
echo "Executing command: $CMD"

exec_cmd_in_netns "$NETNS" $CMD

exit $?
