import evdev

# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#     print(device.path, device.name, device.phys)

dev = evdev.InputDevice("/dev/input/event30")

with dev.grab_context(), evdev.UInput() as ui:
    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            kevent = evdev.categorize(event)
            print(kevent)
            if kevent.scancode == evdev.ecodes.KEY_DOT:
                print("Dot!")
                ui.write_event(event)
                ui.syn()


"""
    @decorator for event matching
    if event not matched, bubble it
    scan for textier vid:pid and create listeners for all devices
    create UInput from device capabilities so able to bubble all unmatched events
    asyncio?
"""