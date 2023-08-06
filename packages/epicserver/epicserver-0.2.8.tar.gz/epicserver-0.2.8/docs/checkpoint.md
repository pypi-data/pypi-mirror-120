# Entity Checkpointing

Applications may explicitly CHECKPOINT their state or leave it to the runtime
to manage saving this. By adding explicit CHECKPOINT calls applications can
guard against failure or unclean execution.

## Persistence Truth Table
      | CHECKPOINT |  Return | Exception
------+------------+---------+-----------
!Dict |   _save()  | _save() | N/A
 Dict |    Dict    |  Dict   | N/A

## Entities
Entites define the state to be persisted via the ```_persist``` attribute
(```List[str]```) as part of the Entity definition. this allows
```Entity._save()``` to know which values to persist to the database and can
be thought of as a schema in database parlance.

Entities may wish to periodically snapshot their state in order to survive
crashes of the runtime, issues with the host or unhandled errors locally. As
per the above [Persistence Truth Table](#persistence-truth-table) above,
uncaught exceptions generated locally will prevent state from being saved.

This may be used to implement rollback by intentionally raising an exception,
it would allow an Entity to try one or more things and if they fail, rely on
the main loops ability to restart the Entity transparently and the
CHECKPOINTing subsystems guarantee to not save state to roll back the
applications to prior to the attempt

=== Example
    ``` python
    class Rollback(Entity):
        @remote_call
        async def update_db(self, key, value, attempts=3):
            if attempts < 0:
                return # database is never comming back

            attempts -= 1
            await CHECKPOINT(locals())

            if not self.db.update(key, value):
                raise ValueError
    ```

## Functions
Functions that have been turned into Entities via ```@callable_entity``` will
have state created for them automatically and kept in sync so that
```Entity._save()``` works transparently. This is achieved by interception of
all syscalls by a wrapper that reads the CHECKPOINT state and applies it to
the created Entities state. This is required so that ```return None``` (or a
if ```return``` is used on its own or omitted) does not cause a reset of the
applications state.

Due to the unknown signature of the state to be persisted it is recommended
that all calls to CHECKPOINT and values returned via ```return``` have the
same keys and are consistent between all Entity Instances
