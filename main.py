import mido
import subprocess
import asyncio

from enum import Enum, unique
from kasa import Discover, SmartPlug


MIDI_PORT = "LPD8 mk2:LPD8 mk2 MIDI 1 20:0"


async def discover_plugs():
    print("Discovering smart plugs...")
    devices = await Discover.discover()
    alias_addr_map = {}
    for addr, dev in devices.items():
        await dev.update()
        alias_addr_map[dev.alias] = addr
    return alias_addr_map


SMARTPLUGS = asyncio.run(discover_plugs())


@unique
class Knobs(Enum):
    KNOB1 = 70
    KNOB2 = 71
    KNOB3 = 72
    KNOB4 = 73
    KNOB5 = 74
    KNOB6 = 75
    KNOB7 = 76
    KNOB8 = 77


@unique
class Pads(Enum):
    PAD1 = 36
    PAD2 = 37
    PAD3 = 38
    PAD4 = 39
    PAD5 = 40
    PAD6 = 41
    PAD7 = 42
    PAD8 = 43


@unique
class Channels(Enum):
    CH1 = 0
    CH2 = 1
    CH3 = 2
    CH4 = 3
    CH5 = 4
    CH6 = 5
    CH7 = 6
    CH8 = 7
    CH9 = 8
    CH10 = 9


@unique
class Programs(Enum):
    PRG1 = 0
    PRG2 = 1
    PRG3 = 2
    PRG4 = 3
    PRG5 = 4
    PRG6 = 5
    PRG7 = 6
    PRG8 = 7


@unique
class Banks(Enum):
    BANK1 = 12
    BANK2 = 13
    BANK3 = 14
    BANK4 = 15
    BANK5 = 16
    BANK6 = 17
    BANK7 = 18
    BANK8 = 19


@unique
class Messages(Enum):
    NOTE_ON = "note_on"
    NOTE_OFF = "note_off"
    CONTROL_CHANGE = "control_change"
    PROGRAM_CHANGE = "program_change"


@unique
class Control(Enum):
    # Knobs
    KNOB1 = (Messages.CONTROL_CHANGE, Knobs.KNOB1, Channels.CH1)
    KNOB2 = (Messages.CONTROL_CHANGE, Knobs.KNOB2, Channels.CH1)
    KNOB3 = (Messages.CONTROL_CHANGE, Knobs.KNOB3, Channels.CH1)
    KNOB4 = (Messages.CONTROL_CHANGE, Knobs.KNOB4, Channels.CH1)
    KNOB5 = (Messages.CONTROL_CHANGE, Knobs.KNOB5, Channels.CH1)
    KNOB6 = (Messages.CONTROL_CHANGE, Knobs.KNOB6, Channels.CH1)
    KNOB7 = (Messages.CONTROL_CHANGE, Knobs.KNOB7, Channels.CH1)
    KNOB8 = (Messages.CONTROL_CHANGE, Knobs.KNOB8, Channels.CH1)

    # Pads
    PAD1 = (Messages.NOTE_ON, Pads.PAD1, Channels.CH10)
    PAD2 = (Messages.NOTE_ON, Pads.PAD2, Channels.CH10)
    PAD3 = (Messages.NOTE_ON, Pads.PAD3, Channels.CH10)
    PAD4 = (Messages.NOTE_ON, Pads.PAD4, Channels.CH10)
    PAD5 = (Messages.NOTE_ON, Pads.PAD5, Channels.CH10)
    PAD6 = (Messages.NOTE_ON, Pads.PAD6, Channels.CH10)
    PAD7 = (Messages.NOTE_ON, Pads.PAD7, Channels.CH10)
    PAD8 = (Messages.NOTE_ON, Pads.PAD8, Channels.CH10)

    # Programs
    PRG1 = (Messages.PROGRAM_CHANGE, Programs.PRG1, Channels.CH10)
    PRG2 = (Messages.PROGRAM_CHANGE, Programs.PRG2, Channels.CH10)
    PRG3 = (Messages.PROGRAM_CHANGE, Programs.PRG3, Channels.CH10)
    PRG4 = (Messages.PROGRAM_CHANGE, Programs.PRG4, Channels.CH10)
    PRG5 = (Messages.PROGRAM_CHANGE, Programs.PRG5, Channels.CH10)
    PRG6 = (Messages.PROGRAM_CHANGE, Programs.PRG6, Channels.CH10)
    PRG7 = (Messages.PROGRAM_CHANGE, Programs.PRG7, Channels.CH10)
    PRG8 = (Messages.PROGRAM_CHANGE, Programs.PRG8, Channels.CH10)

    # Banks
    BANK1 = (Messages.CONTROL_CHANGE, Banks.BANK1, Channels.CH10)
    BANK2 = (Messages.CONTROL_CHANGE, Banks.BANK2, Channels.CH10)
    BANK3 = (Messages.CONTROL_CHANGE, Banks.BANK3, Channels.CH10)
    BANK4 = (Messages.CONTROL_CHANGE, Banks.BANK4, Channels.CH10)
    BANK5 = (Messages.CONTROL_CHANGE, Banks.BANK5, Channels.CH10)
    BANK6 = (Messages.CONTROL_CHANGE, Banks.BANK6, Channels.CH10)
    BANK7 = (Messages.CONTROL_CHANGE, Banks.BANK7, Channels.CH10)
    BANK8 = (Messages.CONTROL_CHANGE, Banks.BANK8, Channels.CH10)

    def __init__(self, message_type, control_id, channel):
        self.message_type = message_type
        self.control_id = control_id
        self.channel = channel


def set_volume(value):
    print(f"Setting volume to {value}%")
    subprocess.run(["amixer", "set", "Master", f"{value}%"])


def set_microphone(value):
    print(f"Setting microphone to {value}%")
    subprocess.run(["amixer", "set", "Capture", f"{value}%"])


def set_left_right_balance(value=64):
    # 0 is full left, 127 is full right
    left = 100 - (value * 100 // 127)
    right = 100 - left
    print(f"Setting left/right balance to {left}%/{right}%")
    subprocess.run(["amixer", "-D", "pulse", "set", "Master", f"{left}%,{right}%"])


def toggle_mute(value):
    print("Toggling mute")
    subprocess.run(["amixer", "set", "Master", "toggle"])


async def toggle_plug(alias):
    plug = SmartPlug(alias)
    await plug.update()
    if plug.is_on:
        await plug.turn_off()
    else:
        await plug.turn_on()


def toggle_plug_sync(alias):
    asyncio.run(toggle_plug(alias))


def toggle_studio_lights(value):
    print("Toggling studio lights")
    toggle_plug_sync(SMARTPLUGS["STUDIO_1"])
    # toggle_plug_sync(SMARTPLUGS["STUDIO2"])


ACTION_MAP = {
    # Knobs
    Control.KNOB1: set_volume,
    Control.KNOB2: set_left_right_balance,
    Control.KNOB3: lambda _: print("Knob 3 pressed"),
    Control.KNOB4: lambda _: print("Knob 4 pressed"),
    Control.KNOB5: set_microphone,
    Control.KNOB6: lambda _: print("Knob 6 pressed"),
    Control.KNOB7: lambda _: print("Knob 7 pressed"),
    Control.KNOB8: lambda _: print("Knob 8 pressed"),
    # Pads
    Control.PAD1: lambda _: print("Pad 1 pressed"),
    Control.PAD2: lambda _: print("Pad 2 pressed"),
    Control.PAD3: lambda _: print("Pad 3 pressed"),
    Control.PAD4: toggle_studio_lights,
    Control.PAD5: lambda _: print("Pad 5 pressed"),
    Control.PAD6: lambda _: print("Pad 6 pressed"),
    Control.PAD7: toggle_mute,
    Control.PAD8: lambda _: set_left_right_balance(64),
    # Programs
    Control.PRG1: lambda _: print("Program 1 selected"),
    Control.PRG2: lambda _: print("Program 2 selected"),
    Control.PRG3: lambda _: print("Program 3 selected"),
    Control.PRG4: lambda _: print("Program 4 selected"),
    Control.PRG5: lambda _: print("Program 5 selected"),
    Control.PRG6: lambda _: print("Program 6 selected"),
    Control.PRG7: lambda _: print("Program 7 selected"),
    Control.PRG8: lambda _: print("Program 8 selected"),
    # Banks
    Control.BANK1: lambda _: print("Bank 1 selected"),
    Control.BANK2: lambda _: print("Bank 2 selected"),
    Control.BANK3: lambda _: print("Bank 3 selected"),
    Control.BANK4: lambda _: print("Bank 4 selected"),
    Control.BANK5: lambda _: print("Bank 5 selected"),
    Control.BANK6: lambda _: print("Bank 6 selected"),
    Control.BANK7: lambda _: print("Bank 7 selected"),
    Control.BANK8: lambda _: print("Bank 8 selected"),
}


def perform_action(control, message):
    print(f"Performing action for {control}")
    action = ACTION_MAP.get(control)
    if action:
        if control.message_type == Messages.NOTE_ON:
            action(message.velocity)
        if control.message_type == Messages.PROGRAM_CHANGE:
            action(message.program)
        if control.message_type == Messages.CONTROL_CHANGE:
            action(message.value)
    else:
        print(f"No action defined for {control}")


def is_matching_message_type(message, control):
    return message.type == control.message_type.value


def is_matching_note_on(message, control):
    return (
        message.type == Messages.NOTE_ON.value
        and message.note == control.control_id.value
    )


def is_matching_control_change(message, control):
    return (
        message.type == Messages.CONTROL_CHANGE.value
        and message.control == control.control_id.value
    )


def is_matching_program_change(message, control):
    return (
        message.type == Messages.PROGRAM_CHANGE.value
        and message.program == control.control_id.value
    )


def is_matching_channel(message, control):
    return message.channel == control.channel.value


def handle_message(message):
    print(f"Handling message: {message}")
    for control in Control:
        if (
            is_matching_message_type(message, control)
            and (
                is_matching_note_on(message, control)
                or is_matching_control_change(message, control)
                or is_matching_program_change(message, control)
            )
            and is_matching_channel(message, control)
        ):
            print(f"Received {control}")
            perform_action(control, message)
            break
        else:
            print(f"Message not recognized: {message}")


if __name__ == "__main__":
    with mido.open_input(MIDI_PORT) as inport:
        print(f"Listening on {MIDI_PORT}...")
        for message in inport:
            print(f"Message: {message}")
            handle_message(message)
