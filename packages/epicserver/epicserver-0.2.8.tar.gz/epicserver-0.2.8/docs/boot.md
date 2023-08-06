# Application Deployment Compatibility

There are several deployment options and caveats when administrering an EpicMan
Server cluster. Below is a quick guide to cluster deployment options and the 
compatible ways to launch an application on the cluster Other deployment and
startup methods exist but are not supported.

            | Single | Local | Network
------------+--------+-------+---------
.py file    |   ✓    |   ✓   |    ❌
.py minimal |   ✓    |   ✓   |    ✓
module      |   ✓    |   ✓   |    ✓


## Deployment Option

### Single

A single EpicMan process that directly specfies the startup script and uses none
of the clustered features

### Local

Multiple EpicMan processes in clustered mode that exist on the same machine AND
use the same ennvironment AND run out of the same base directory (This last 
requirement is to support running startup scripts in the working directory).

### Network

Multiple EpicMan processes with one or more processes on a remote node without
a shared filesystem. If the filesystem is shared then this is more like the 
(local)[#Local] install specified above. Note: the filesystem may be considered 
'shared' by out of band sync such as git or rsync on deployment.


## Startup code type

### .py file

A python script that defines one or more entities and an entry point that when 
specified via import path (the last argument to the EpicMan Server process), is
used to start up the application environment.

### .py minimal

This is identical to the above but does not specifiy any entities. This may be
a thin wrapper that does some basic checks then calls an already installed 
module or takes steps to bootstrap the rest of the environment (eg sync code to
remote nodes)

### module

This is a standard python package on sys.path that can be imported normmaly and
is usually managed or installed by an application such as pip.
