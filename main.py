import mido
import subprocess

from enum import Enum, unique


MIDI_PORT = "LPD8 mk2:LPD8 mk2 MIDI 1 20:0"


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


@unique
class Messages(Enum):
    NOTE_ON = "note_on"
    NOTE_OFF = "note_off"
    CONTROL_CHANGE = "control_change"


@unique
class Control(Enum):
    # Knobs
    KNOB1 = (Messages.CONTROL_CHANGE, Knobs.KNOB1, Channels.CH1)
    KNOB5 = (Messages.CONTROL_CHANGE, Knobs.KNOB5, Channels.CH1)

    # Pads
    PAD1 = (Messages.NOTE_ON, Pads.PAD1, Channels.CH1)

    def __init__(self, message_type, control_id, channel):
        self.message_type = message_type
        self.control_id = control_id
        self.channel = channel


def set_volume(value):
    print(f"Setting volume to {value}%")
    subprocess.run(["amixer", "set", "Master", f"{value}%"])

def set_microphone(value):
    print(f"Setting microphone to {value}%")
    subprocess.run(["amixer", "set", "Mic", f"{value}%"])


ACTION_MAP = {
    Control.KNOB1: set_volume,
    Control.KNOB5: set_microphone,
    # Add other controls with their actions
}


def perform_action(control, message):
    print(f"Performing action for {control}")
    action = ACTION_MAP.get(control)
    if action:
        if control.message_type == Messages.NOTE_ON:
            action(message.velocity)
        if control.message_type == Messages.CONTROL_CHANGE:
            action(message.value)
    else:
        print(f"No action defined for {control}")


def is_matching_message_type(message, control):
    return message.type == control.message_type.value


def is_matching_note_on(message, control):
    return message.type == Messages.NOTE_ON.value and message.note == control.control_id.value


def is_matching_control_change(message, control):
    return message.type == Messages.CONTROL_CHANGE.value and message.control == control.control_id.value


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
