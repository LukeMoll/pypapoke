import evdev # type: ignore
import asyncio

from typing import List, Dict, Callable

def find_devices_by_vidpid(vid : int, pid : int) -> List[evdev.InputDevice]:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    return list(filter(lambda d: d.info.vendor == vid and d.info.product == pid, devices))

key_bindings : Dict[int,Callable[[evdev.KeyEvent], None]] = {}

async def device_reader(dev : evdev.InputDevice):
    with dev.grab_context(), evdev.UInput.from_device(dev) as ui:
        async for event in dev.async_read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                kevent = evdev.categorize(event)
                print(kevent)
                if kevent.scancode in key_bindings:
                    key_bindings[kevent.scancode](kevent)
                else:
                    ui.write_event(event)
                    ui.syn()
            else:
                ui.write_event(event)
                ui.syn()

def handler(scancode : int):
    if scancode in key_bindings:
        raise Exception(f"Handler already registered for {scancode}!")
    def __decorator(fn : Callable[[evdev.KeyEvent], None]):
        key_bindings[scancode] = fn

    return __decorator

if __name__ == "__main__":
    @handler(evdev.ecodes.KEY_DOT)
    def dot_handler(kev : evdev.KeyEvent):
        if kev.keystate == evdev.KeyEvent.key_up:
            print("Dot!")

    for inputdevice in find_devices_by_vidpid(0x239a, 0x80aa):
        print(inputdevice.path, inputdevice.name, inputdevice.phys)
        asyncio.ensure_future(device_reader(inputdevice))

    loop = asyncio.get_event_loop()
    loop.run_forever()

"""
    scan for textier vid:pid and create listeners for all devices
"""