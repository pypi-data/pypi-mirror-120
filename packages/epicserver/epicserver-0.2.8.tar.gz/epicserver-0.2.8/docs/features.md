## Features

## For Admins
* Alleviate performance issues by simply adding more Application servers
* Automatic Server discovery and setup
* Support for multiple database backends
* Ability to run multiple seperate clusters on the same hardware

## For Developers
* Virtual Actor based Framework
* Focus on single large distributed game worlds
* Simple async/await based syntax for messaging between entities
* Automatic persistence of game object state to databases
* Various messaging based constructs including
  * One way messaging
  * RPC
  * Streaming values (networked iterators)
  * Pub/Sub
* Takes care of most of the clustering and monitoring for you

Applications running on this Framework consist of 2 parts, the Server as
provided by this module [epicserver](http://pypi.org/project/epicserver) and
the user code/App running on top of this. Multiple Apps can be running to help
facilitate middleware without explicitly bundling it into your application.

## Feature Requests
The documentation is regularly updated with a [roadmap] as well as [todo] and 
[bugs]. If there is a feature you need or want this is the first place to 
check to see if it has already been planned and scheduled for release.

Due to licensing and code ownership issues we do not generally accept 3rd 
party patches and will generally reimplement them for the aforementioned 
licensing issues and to ensure they meet our standards for maintainability (ie 
tested, meet style guidelines and are writing in a way we feel we can continue 
to maintain in the future).

If you do find a bug or security issue please contact us at 
placeholder@example.org and provide a brief description of what you did to 
cause the issue, why it is an issue (as it may not be clear to us, eg 
non-obvious behaviour) and reproducible test cases if any.

If you require a specific feature not on our roadmap then do not hesitate to 
reach out.

Commercial support is available.
