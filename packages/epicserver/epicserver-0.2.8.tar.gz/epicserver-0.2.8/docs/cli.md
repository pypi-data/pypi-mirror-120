# CLI Arguments

=== "Full output"
    ``` console
    --8<-- "docs/cli_output.md"
    ```

!!! warning "idna Domains"
    All arguments that accept a domain or host name convert the value to an
    idna compatible representation and native domains can be used without
    manual translation. Translation may be required when running non
    interactively such as under service management like systemd where the
    ```$LANG``` variable may not be the same as for interactive/GUI usage (and
    likely set to ```LANG=C``` or ascii). If this is the case the translated
    idna name sill need to be used in the service management files.


!!! note "entrypoint"
    EpicMan Server is designed to run other user provided applications, this
    argument allows you to specify what code is to be run on the server in a format
    similarly to entry hooks.

    The format is made up of 2 parts separated by a ":", a module path on the left
    hand side and a function name on the right hand side. As a rule of thumb, if
    it can fit into the template from ```<-: import :->``` then it is likely valid
    where <-: and :-> refer to the left and right hand side of ":" respectfully

    === "Example"
        ``` python
        epicman-sever epicman.game:start_app
        ```

    The convention is to call your application entry point 'start_app' which will
    be spawned as instance '0', this may exit as long as other processes are
    running or IO is occurring. start_app can optionally be omitted and be
    equivalent to the invocation above as shown below

    === "Example"
        ``` python
        # Identical to earlier example
        epicman-sever epicman.game:
        ```


!!! note "[-v|--verbose]"
    EpicMan Server has multiple different levels of verbosity, starting at ERROR
    then WARN, INFO and finally DEBUG. specifying this flag one or more times
    will increase the amount that is logged. Note: this has a performance impact
    as most messages are discarded without processing in the default (ERROR)
    level.


!!! note "[-n|--name] NAME"
    The name of the cluster when communicating over the network. This allows
    multiple clusters to share the same network and prevents inter-connection from
    2 different clusters running on the same network.


!!! note "[-l|--listen] ADDR"
    The listen address for incoming server to server connections when running an
    application across more than one node.

    This argument accepts a address:port argument pair. Additionally the address
    or port may be omitted to use a default value


!!! note "[-b|--bootstrap] ADDR[,ADDR[...]]"
    Clustered nodes send messages between themselves about all the members in the
    cluster. At startup this information is not present and the bootstrap nodes
    listed here are used to get an initial list of cluster members so that a new
    process may join the cluster.

    This argument expects a comma separated list of address:port pairs


!!! note "[-c|--cpu] CPU"
    Set the CPU affinity mask for the process. Ideally this should be done by the
    invoker such as Systemd, however there are times (eg with polyinstanciated
    units) where you want a core per node and do not want the cpu to be shared.
    This option can be used to facilitate this.

    for polyinstanciated units it is expected that the instance name after the
    @ in the service file is an integer that corresponds 1:1 with a cpu core,
    eg ```epicman-server@2.service```, the instance name can then be passed in
    directly to the ```--cpu``` argument.


!!! note "[-d|--database] URL"
    bdb, in memory dictionaries and sqlite. The most appropriate backend depends on
    the application, performance and durability you need for your application (See
    [Databases] for more info).

    This option allows you to specify which db backend, the location to it on disk
    (if any) and additional backend specific options.
