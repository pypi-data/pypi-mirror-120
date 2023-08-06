## Where code lives and who is responsible for each part
```
  +--------+         +---------------------------------+
  | Client |-----\  +---------------+  +-------------+ |
  +--------+     +--| Server Socket |--| Application | |
                 |  +---------------+  |    Logic    | |
  +--------+     |   |                 |             | |
  | Client |-----|   |                 | * Entity    | |
  +--------+     |   |   Application   | * Entity    | |
                 |   |     Server      | * Entity    | |
  +--------+     |   |                 |             | |
  | Client |-----/   |                 +-------------+ |
  +--------+         +---------------------------------+
                            ^
Provided by User <-|        |        |-> Provided by User
                      EpicMan Game
```

## Physical topology of servers
```
========================= Network ========================
        |                    |                    |
        |                    |                    |
 +-------------+      +-------------+      +-------------+
 | Application |      | Application |      | Application |
 |    Server   |      |    Server   |      |    Server   |
 |+-----------+|      |+-----------+|      |+-----------+|
 ||   Entity  ||      ||   Entity  ||      ||   Entity  ||
 |+-----------+|      |+-----------+|      |+-----------+|
 ||   Entity  ||      ||   Entity  ||      ||   Entity  ||
 |+-----------+|      |+-----------+|      |+-----------+|
 ||   Entity  ||      ||   Entity  ||      ||   Entity  ||
 |+-----------+|      |+-----------+|      |+-----------+|
 ||   Entity  ||      ||   Entity  ||      ||   Entity  ||
 |+-----------+|      |+-----------+|      |+-----------+|
 +-------------+      +-------------+      +-------------+
 ID: 4217be89c88      ID: 02ecb190c63      ID: edb5e1069dd
   [ Server 1 ]         [ Server 2 ]         [ Server 3 ]
```


## Mapping of Entites to the server that owns them
```
                +-------------+        +-----------------------+
                | 00000000000 |<-------| Entity ID=16bf1cd7662 |
 [ Server 2 ]---|             |        +-----------------------+
                | 02ecb190c63 |  /-----| Entity ID=2d8b236ac9c |
                +-------------+  |     +-----------------------+
 [ Server 1 ]---|             |<-/  /--| Entity ID=aa15b1c4a82 |
                | 4217be89c88 |     |  +-----------------------+
                +-------------+     |  | Entity ID=859a559a417 |
                |             |     |  +-----------------------+
                |             |<----+  | Entity ID=a69dc2d1abf |
 [ Server 3 ]---|             |     |  +-----------------------+
                |             |     |  | Entity ID=1c82c38af8b |
                |             |     |  +-----------------------+
                | edb5e1069dd |     \--| Entity ID=b08b717b25f |
                +-------------+        +-----------------------+
```


## Objects
*[Entity]: An Entity that represents an object running on the mesh, each Instance has an Address to help locate it.
*[Address]: A combination of Namespace and Instance to locate a specific object on the mesh, this may be local or on another Node
*[Namespace]: There may be multiple different objects communicating on the Mesh each with their own idea of an Instance which may overlap with each other. the Namespace is used to disambiguate these and allow overlapping Instance spaces
*[Instance]: Which specific instance of a Namespace and Address points to

## Server
*[Mesh]: A group of Nodes can connect to each other and form a mesh. This Mesh can then be used to run Entities distributed over the network with EpicMan Server handling communication between Nodes and providing the illusion of all processes running locally.
*[Node]: A single EpicMan Server instance in a Mesh. Provides basic IO and Networking facilities and communication abstractions to transparently communicate with all other nodes
