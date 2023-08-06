
## DNSCache

This points to (LocalDNSCache)[#LocalDNSCache] by Default, see below for more 
details.

## LocalDNSCache

LocalDNSCache and ClusterDNSCache are identical in all aspects except that 
LocalDNSCache exposes a hint to the scheduelr to ensure that all isntances are 
run locally. This has the effect of making all DNS lookups that are cached 
local to this EpicMan Node only.

If used within a cluster this may cause extra DNS requests to be sent to a 
resolver but may also have increased performance if the same query is requeted 
multiple times as it will not have to make a network round trip to look up the 
anwser.


## ClusterDNSCache

ClusterDNSCache lifts the requirment that all Entities in this namespace must 
execute locally. This will distribute the lookup and caching of DNS Quiries 
over the entire cluster.

If the clsuter is geo distributed then this may cause issues with Geo 
targeting DNS servers and may cause web requests to server up incorrectly 
localized data or requests to go to a non optimal server.

Fast DNS servers are avalible and cachign servers that scale to 1000's of 
requests per second are easy to set up and as such it is expected this will 
have limited utility execpt in a few specific cases.

## Getname

This is intended to be a simple interface to use that backs on to getaddrinfo.
This is primarily intended to be used for simple lookups or where compatibility
witht he system configuration is require.

For most applications this should be the default choice as the behavior of the 
DNSCaches may be subtly diffrent to normal application development.


## Which to chose

The optimal type of cache to chose is going to be highly application 
dependent. it is recomended to start with The default ((DNSCache)[#DNSCache]) 
which is Local by default and move to the clustered solution if DNS lookups 
become the bottleneck. Where the clustered mode really shines is lots of 
requests for the same resouces by Entites spread all over the cluster. If 
however a particiualr node is likley to be making lots of identical lookups 
and other nodes make diffrent lookups (Eg a single Entity performing work on a 
subset of domains) then the LocalDNSCache may be more performant
