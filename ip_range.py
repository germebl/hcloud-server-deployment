# ip_range.py
import sys
from ipaddress import ip_network

network = ip_network(sys.argv[1])
ips = [str(ip) for ip in network.hosts()]
print(",".join(ips))
