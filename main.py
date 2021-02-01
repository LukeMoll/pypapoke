import asyncio
from evdev import ecodes, KeyEvent
from .keybind import handler, find_devices_by_vidpid, device_reader
from .backend_pactl import PACtlBackend

pulse = PACtlBackend()

sinks = pulse.get_sinks()
sink_speakers = next(filter(lambda t: "hdmi" in t[1].lower(), sinks))
sink_headphones = next(filter(lambda t: "behringer" in t[1].lower(), sinks))

@handler(ecodes.KEY_DOT)
def dot_handler(kev : KeyEvent):
    if kev.keystate == KeyEvent.key_up:
        print("Dot!")

@handler(ecodes.KEY_F1)
def to_headphones(kev : KeyEvent):
    if kev.keystate == KeyEvent.key_up:
        pulse.move_sink_inputs_to(sink_headphones[1])

@handler(ecodes.KEY_F2)
def to_speakers(kev : KeyEvent):
    if kev.keystate == KeyEvent.key_up:
        pulse.move_sink_inputs_to(sink_speakers[1])

if __name__ == "__main__":
    for inputdevice in find_devices_by_vidpid(0x239a, 0x80aa):
        asyncio.ensure_future(device_reader(inputdevice))

    loop = asyncio.get_event_loop()
    loop.run_forever()