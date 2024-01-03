_This is my blog part 1 of 3 for the v0.4 release of Space War RL!_

I recently discovered [pygbag](https://pypi.org/project/pygbag/) that allows my game/sim to be playable from the browser.

You can play my stable version [here](https://e-dong.itch.io/spacewar). You can play my dev version [here](https://e-dong.itch.io/spacewar-dev).

## What is pygbag?

TBA

## Issues/Challenges I faced

### Patching pygame.time.set_timer

Due to [pygbag#16](https://github.com/pygame-web/pygbag/issues/16), the built-in function does not work correctly in the `pygbag-wasm` environment.

I made an improvement to the patch by handling other behaviors mentioned in the docs:

```python
def patch_timer():
    # pylint: disable-next=import-outside-toplevel
    import asyncio

    # pylint: disable-next=import-error,import-outside-toplevel
    import aio.gthread

    # Global var to keep track of timer threads
    #   - key: event type
    #   - value: thread uuid
    THREADS = {}

    def patch_set_timer(
        event: Union[int, pygame.event.Event], millis: int, loops: int = 0
    ):
        """Patches the pygame.time.set_timer function to use gthreads"""

        dlay = float(millis) / 1000
        cevent = pygame.event.Event(event)
        event_loop = asyncio.get_event_loop()

        async def fire_event(thread_uuid):
            """The thread's target function to handle the timer

            Early exit conditions:
            - event loop is closed
            - event type is no longer in THREADS dictionary
            - the thread's uuid is not the latest one
            - Max loop iterations if loops param is not zero
            """
            loop_counter = 0
            while True:
                await asyncio.sleep(dlay)
                if (
                    event_loop.is_closed()
                    or event not in THREADS
                    or THREADS[event] != thread_uuid
                    or (loops and loop_counter >= loops)
                ):
                    break

                pygame.event.post(cevent)
                loop_counter += 1 if loops else 0

        if dlay > 0:
            # uuid is used to track the latest thread,
            # stale threads will be terminated
            thread_uuid = uuid.uuid4()
            Thread(target=fire_event, args=[thread_uuid]).start()
            THREADS[event] = thread_uuid

        else:
            # This cancels the timer for the event
            if event in THREADS:
                del THREADS[event]

    pygame.time.set_timer = patch_set_timer


if platform.system().lower() == "emscripten":
    patch_timer()
```
