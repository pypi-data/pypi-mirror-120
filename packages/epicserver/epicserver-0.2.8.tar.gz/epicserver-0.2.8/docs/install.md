# Installation

## Requirements

EpicMan Server has been writen with a minimal set of dependencies in mind and
3rd party features are optional. 

* Python 3.7 or newer
* A 64 bit CPU if the lmdb backend is in use
* Linux 5.x or newer (required for io_uring backend)
* Kernel headers may be required to compile the python [liburing](https://pypi.org/project/liburing) module

## Creating a VirtualEnv (Optional)
``` console
$ python3 -m venv venv
# Activate the virtualenv to use commands and libraries in it
$ . venv/bin/activate
(venv) $
```

## Installing EpicMan Server
``` console
(venv) $ venv/bin/pip install epicman
```

## Installing Optional Extras
``` console
(venv) $ venv/bin/pip install epicman[lmdb]
```

## Starting the Server
``` console
(venv) $ epicman-server epicman.game.examples.ping_test:game_start
```
** Use ctrl+c to terminate the server **

