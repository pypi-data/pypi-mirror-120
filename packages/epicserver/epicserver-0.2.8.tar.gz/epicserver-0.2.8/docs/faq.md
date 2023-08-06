## Why does this exist?

I wanted to build a single instance game world that exceeded the size/scope of 
a single hardware chassis or vitual machine. This project began pre-Docker and 
the original virtual hosting/private instance work used Linux's first 
container impelementations directly

### Data placement and routing
Modern development strategies from the Web world that have scince come along 
would have engineered this project slightly diffrently however due to the 
nature of the problem space (Games) and the scope, It was felt there was a 
need to stick to the orignal design and handle many of the data managment 
features internally as this stack is greatly affected by messaging latency. 
Having control over data placemnt and message routing allows us to exploit 
locailty better and attempt to keep processing in-process

### Overcomming Pythons GIL in novel ways via shared nothign and messaging
CPython has an internal lock that provents Parrallelism limiting most normal 
python code to a single core. Due to the internal entity model and message 
sending abstrctions it made it simple to slide a network shim in there and 
present abstraction that all entites are local. Once Entites have mobile 
placemnt in this manner they are no longer restricted by the GIL so long as 
they are not executing int he same process which can be leaveraged for both 
parallism and fault tollerence (See Erlang below for other languages that do 
this). This can also allow code to be freed from the limitations of the 
ammount of memory in a single chassis.

### Keeping things simple
By Keeping thigns simple i am talking about overall holistic system complexity 
which I (Blitz Works) Feels is commonly overlooked in modern solutions 
developed by programers with no or minimal system complexity and exisbated by 
layering and abstraction. This framework has been more than willing to take on 
100 lines of code to avoid 1000's to 10000's of lines of code as a dependency. 
This not only extends to minimal dependencies beyond the stdlib but also in 
the deployment and Continous Intergration/Testing pipeline but also the 
runtime itself (eg using AWS services counts as pulling in all of AWS in this 
context).

It should be possible to run and develop for this project from a checkout and 
a handful of dependncies AND develop productivly with no internet access. 
Somthing that comes up more often than one would think as outages seem to 
become increasingly acceptable to people. This is also relvant to other 
communites without access to cheap and plentiful access to fast low latency 
internet.

### I do crazy things
I have a number of projects that push python to its absoulte limits and this 
is the most ambitous of them. This has mostly seemed like a good idea with 
many unknowns and if this project serves as a warning to others in its failure 
then it has more than achived its goal.

## EpicServer wont start complaining about lack of IPv6 support

EpicServer is an IPv6 Native or IPv6 first product and requires IPv6 and IPv6 
Dual stack support for your oprerating system. For the Operating systems below 
this should work out of the box.

* Windows
* Mac OSX

For the following operating systems additional work may be required as this 
may be disabled.

* Linux
* FreeBSD
* OpenBSD

IPv6 Dual stack is used to send IPv4 traffic via IPv6 sockets as it is easier 
to write and maintain an application that support IPv4 via IPv6 than it is to 
write an IPv4 application that also supports IPv6. This has to do with 
unication of code paths in the former solution vs having to special case many 
seperate instances in the second case that are littered all over the code base 
and user code.

## Isnt IPv6 insecure? The internet says to disable it

Many people forget IPv6 is seperate to IPv4 and an IPv4 firewall will not 
protect IPv6 and has to be configured seperatly. In addition IPv6 is diffrent 
enougha nd can be depoyed in a few additinal ways beyond what is avliable for 
IPv4 meaning that firewalls are not a stright forward port from IPv4 to IPv6

Rather than disabling the IPv6 module as is recomended in most guides we 
instead recomend setting the default INPUT and FORWARD policy to DROP under 
linux if you do not intend to use IPv6 as this allows IPv6 sockets to still be 
used to send IPv4 traffic (via the magic address ::FFFF:<IPv4 Addr>, eg 
::FFFF:10.0.0.1) without having to detirmine an appririate IPv6 
setup/deployment for your systems.

## This looks a lot like Erlang

[Erlang](https:/www.erlang.org) was leant upon for some of the design aspects 
and other sources of insperation for this project also hevily borrowed from 
Erlang. If managing a cluster or programing for EpicServer then taking a look 
into how Erlang works is recomended and may inspire solutions to some day to 
day problems not covered in this documentation.

## This looks a lot like Microsofts Orleans Framework

This was primarly based off Microsofts Orleans framework and also borrowed 
some ideas from 2 other projects by Microsoft Research, Namley Barrelfish and 
Singularity. Some of the concepts of LINQ where also borroed from the .net 
family of languages.

## Some of this Looks like ZODB/ZopeDB or Durus

While writing a ZODB/Durus clone many of the design aspects of this framework 
came up. There is an additional project to implement a persistant store on top 
of EpicServer beyond the in built Entity persitance as a seperate repository 
that also reuses parts of LINQ as mentioned in earlier questions. If you think 
this sounds a bit like mensia from Erlang then you would be correct and while 
not the main inspiration for this, it has served as a useful refrence on both 
implementation, managment and usage fronts

## What are these extra fields in S2S IPv6 connectiosn that sometimes appear?
```
[S2S:IPv6Address('::1'), 42892, 0, 0]
```

vs

```
[S2S:IPv6Address('::1'), 3030]
```

the '0, 0' will normally only be visible on incoming connections and 
represent the 'IPv6 Flow' and 'Interface number', these are IPv6 only concepts 
that can mostly be ignored.

One exception to this is 'Link Local Addresses' such as 
fe80::b07b:a934e:5b44:5353 or any address starting with fe80:. These represent 
non routable addresses that exists on every interface. As these addresses (and 
corresponding IPv6 Range) exist on every interface the second '0' is used to 
distinguish which interface to send and receive traffic for that connection as 
it cannot be determined purely from the routing table (as the same route now 
exists on every interface creating ambiguity, this field is the tie breaker 
for that ambiguity)

There are few good reasons to use link local addresses and the one case where 
this would apply (clusters on 2 separate interfaces) would cause networking 
issues and cluster split brain as nodes on each interface would not be able to 
communicate with nodes on the other interface as these addresses are 
unroutable between interfaces. As such they are only a good indicator of a 
broken network and therefore for debugging the scenario outlined above.
