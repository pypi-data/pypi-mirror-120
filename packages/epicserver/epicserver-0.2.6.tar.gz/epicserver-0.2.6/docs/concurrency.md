EpicMan Server uses a concurrency model similar to AsyncIO and similar 
frameworks (eg Trio and Curio). This is due to using the same asynchronous 
primitives, namely async/await.

Due to the Server running the game code on a single thread on a single node at 
a time, any code executing between 2 awaits has exclusive access to the entity 
state and will not be preempted. 

For simple updates (eg updating a list) having this occur between await's 
means this will be atomic from the perspective of other Entities or other 
instances of the same Entitiy (ie if multiple calls to the Entity are in 
flight at the same time).

=== "Entity with exclusive access periods annotated"
    ``` python
    class Obj(Entity):
        shared_list = []
        
        async def update():
            # Start exclusive access      # |
            do_thing()                    # |
            some_math()                   # |
            # End exclusive access        # |

            client = await TASK_RECV()    # + await denotes exclusive access
            # Start exclusive access      # |
            shared_list.append(client)    # |
            # End exclusive access        # |
            await TASK_SEND(client, 'ok') # + await denotes exclusive access

            # Start exclusive access      # |
            cleanup()                     # |
            # End exclusive access        # |
    ```


If atomicity is required across await's then locking must be performed. This 
is currently unimplemented. It is possible to emulate with TASK_RECV and a 
list of tasks to wake up. The implementation of this alternate solution is 
left up to the reader until primitives become available.

=== "Proposed locking mechanism"
``` python
class Obj(Entity):
    shared_list()
    
    # Note this is advisory locking not mandatory locking
    # any object not participating in this proctor explicitly will bypass it
    async def update(self):
        self.listen(('localhost', 3030))
        with locking(self.shared_list) as l:
            async for client in self.recv(): # async for uses await under the hood
                l.append(client)
```
