# Welcome to EpicMan Server

EpicMan Server is an application server based of the Virtual Actor Orleans
framework from Microsoft Research
[link](https://dotnet.github.io/orleans/docs/). EpicMan Server provides an
Asynchronous IO loop of its own design and runs async functions or Entity
sub-classes from this event loop providing inter Entity messaging that can
optionally extend across the network.

At a high level, EpicMan Server builds a mesh of python processes across
multiple machines upon which your code is distributed across with the server
providing an messaging abstraction that takes care of the individual details
of starting your code and its entities and distributing them across the
network.

This was mainly written to support [EpicMan Game](http://www.epic-man.com)
however the Virtual Actor design and persistence to database backends lend
itself to other applications such as webservers, chat servers, storage meshes
or anything message heavy and/or maps to Key/Values pairs.

## Stack

EpicMan Server attempts to be as self contained as possible with 3rd party 
systems being optional dependencies. The tech stack consists of:

* Python 3.7+
* Linux 5.x+
* SQLite or lmdb for persistence [Optional]

This does not prevent you from plugging in your own existing libraries and 
infrastructure. EpicMan Server has built in integration points that leverage 
entry_points to allow you to use your existing infrastructure as simply as 
```pip installing``` a package.

Currently entry points exist for:
* Application/Game code that is run on startup
* Database used for the persistence layer

with network serialisation to be added in the future.


## Getting Started

If you are looking to run and manage a cluster then start at [Managing a Cluster](install.md).

If you are looking to develop an App that runs on the framework then the [API](entities.md)
Documentation will be handy reference as well as the [Development](concepts.md)
documentation to get a feel for how the code base is laid out.

If you are just looking to add new features to the Epic Server Code or fix
bugs then take a look at the [Development](concepts.md) documentation.
