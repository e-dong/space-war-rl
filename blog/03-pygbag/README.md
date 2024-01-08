_This is my blog part 1 of 3 for the v0.4 release of Space War RL!_

Normally games made with `pygame` are not playable from the web. They can only be run from the command line or use [PyInstaller](https://pyinstaller.org/en/stable/) or [cx_Freeze](https://cx-freeze.readthedocs.io/en/latest/) to create a standalone executable (e.g. .exe file)

I recently discovered [pygbag](https://pypi.org/project/pygbag/) that allows python code to run in a web browser.

You can play my stable version [here](https://e-dong.itch.io/spacewar). You can play my dev version [here](https://e-dong.itch.io/spacewar-dev).

## Stable Version

This build will follow my latest [github releases/tags](https://github.com/e-dong/space-war-rl/releases).

## Dev Version

This build will serve as my testing grounds for new features to solicit more feedback. At the time of writing this post, the dev version contains weapons, ship collisions, and more. My next 2 blog posts in this series will cover my updates.

## What is pygbag?

Pygbag is a C runtime linked to cython-wasm compiled to WebAssembly by Emscripten and hosted on pygame-web.github.io. You can read more about pygbag on their [wiki page](https://pygame-web.github.io/). You can see some demos [here](https://pygame-web.github.io/#demos-on-itchio-).

## Issues/Challenges I faced

### Patching pygame.time.set_timer

Due to [pygbag#16](https://github.com/pygame-web/pygbag/issues/16), the built-in function does not work correctly in the `pygame-wasm` environment.

I made an improvement to the patch by handling other behaviors mentioned in the [docs](https://pyga.me/docs/ref/time.html#pygame.time.set_timer):

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

I created a `THREADS` dictionary to keep track of all the spawned threads. It is keyed by the event type and contains the uuid of the thread. A delay of 0 will cancel the timer by deleting the event type from the dictionary, which causes the while loop to break in the `fire_event` function. If there are multiple threads for the same event type, only the latest one is considered due to this condition in the if block: `THREADS[event] != thread_uuid`.

This is only a temporary workaround until a fix is completed upstream.
