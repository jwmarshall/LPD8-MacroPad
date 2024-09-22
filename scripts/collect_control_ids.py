import mido

MIDI_PORT = 'LPD8 mk2:LPD8 mk2 MIDI 1 20:0'

def collect_control_ids(port_name):
    with mido.open_input(port_name) as inport:
        print(f"Listening on {port_name}... Interact with each control to record its ID.")
        print("Press Ctrl+C to stop.")
        try:
            for message in inport:
                if message.type in ['note_on', 'control_change']:
                    control_id = message.note if message.type == 'note_on' else message.control
                    channel = message.channel
                    print(f"Type: {message.type}, ID: {control_id}, Channel: {channel}")
                    control_name = input("Enter a name for this control (or press Enter to skip): ")
                    if control_name:
                        control_mappings.append({
                            'name': control_name,
                            'type': message.type,
                            'id': control_id,
                            'channel': channel
                        })
        except KeyboardInterrupt:
            print("Control ID collection stopped.")

if __name__ == "__main__":
    control_mappings = []
    collect_control_ids(MIDI_PORT)
    # Save the mappings to a file or print them out
    for mapping in control_mappings:
        print(mapping)

