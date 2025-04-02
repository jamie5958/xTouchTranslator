import rtmidi
from ConfigManager import ConfigManager

class SysexController:
    def __init__(self, midi_out, page_manager):
        """
        Initialize the SysExController with a MIDI output device.
        :param midi_out: An instance of rtmidi.MidiOut
        """
        self.midi_out = midi_out
        self.config_manager = ConfigManager()
        self.page_manager = page_manager

    def send_sysex_message(self, message):
        """
        Send a SysEx message to the MIDI output device.
        :param message: A list of integers representing the SysEx message.
        """
        if not self.midi_out:
            print("MIDI Out device is not initialized.")
            return

        try:
            self.midi_out.send_message(message)
            print(f"Sent SysEx message: {message}")
        except Exception as e:
            print(f"Failed to send SysEx message: {e}")

    def write_to_scribble_strip(self, page_index, channel, color, second_line_inverted, line_one_text, line_two_text):
        """
        Write text to the scribble strip of a specific channel.
        :param channel: The channel number (0-7).
        :param text: The text to display on the scribble strip.
        """
        if not self.midi_out:
            print("MIDI Out device is not initialized.")
            return
        
        # Convert channel to appropriate byte value
        if 0 <= channel <= 7:
            if channel == 0:
                self.channel = 0x20  # Channel 1 (0x20)
                print("Channel set to 1")
            elif channel == 1:
                self.channel = 0x21  # Channel 2 (0x21)
                print("Channel set to 2")
            elif channel == 2:
                self.channel = 0x22  # Channel 3 (0x22)
                print("Channel set to 3")
            elif channel == 3:
                self.channel = 0x23  # Channel 4 (0x23)
                print("Channel set to 4")
            elif channel == 4:
                self.channel = 0x24  # Channel 5 (0x24)
                print("Channel set to 5")
            elif channel == 5:
                self.channel = 0x25  # Channel 6 (0x25)
                print("Channel set to 6")
            elif channel == 6:
                self.channel = 0x26  # Channel 7 (0x26)
                print("Channel set to 7")
            elif channel == 7:
                self.channel = 0x27  # Channel 8 (0x27)
                print("Channel set to 8")
        else:
            print("Invalid channel. Must be between 0 and 7.")
            return
        
        if second_line_inverted == True or second_line_inverted == False:
            self.second_line_inverted = second_line_inverted
        else:
            print("Invalid second line inverted value. Must be True or False.")
            return

        # Convert color and second line inverted to appropriate byte values
        if color == "red":
            if not second_line_inverted:
                self.color = 0x01  # Red (0x01)
                print("Color set to Red")
            elif second_line_inverted:
                self.color = 0x41  # Red inverted (0x41)
                print("Color set to Red (Inverted)")
        elif color == "green":
            if not second_line_inverted:
                self.color = 0x02  # Green (0x02)
                print("Color set to Green")
            elif second_line_inverted:
                self.color = 0x42  # Green inverted (0x42)
                print("Color set to Green (Inverted)")
        elif color == "yellow":
            if not second_line_inverted:
                self.color = 0x03  # Yellow (0x03)
                print("Color set to Yellow")
            elif second_line_inverted:
                self.color = 0x43  # Yellow inverted (0x43)
                print("Color set to Yellow (Inverted)")
        elif color == "blue":
            if not second_line_inverted:
                self.color = 0x04  # Blue (0x04)
                print("Color set to Blue")
            elif second_line_inverted:
                self.color = 0x44  # Blue inverted (0x44)
                print("Color set to Blue (Inverted)")
        elif color == "pink":
            if not second_line_inverted:
                self.color = 0x05  # Pink (0x05)
                print("Color set to Pink")
            elif second_line_inverted:
                self.color = 0x45  # Pink inverted (0x45)
                print("Color set to Pink (Inverted)")
        elif color == "cyan":
            if not second_line_inverted:
                self.color = 0x06  # Cyan (0x06)
                print("Color set to Cyan")
            elif second_line_inverted:
                self.color = 0x46  # Cyan inverted (0x46)
                print("Color set to Cyan (Inverted)")
        elif color == "white":
            if not second_line_inverted:
                self.color = 0x07  # White (0x07)
                print("Color set to White")
            elif second_line_inverted:
                self.color = 0x47  # White inverted (0x47)
                print("Color set to White (Inverted)")
            self.color = 0x47  # White inverted (0x47)
            print("Color set to White (Inverted)")
        elif color == "off":
            self.color = 0x00  # Off (0x00)
            print("Color set to Off")
        else:
            print("Invalid color. Must be one of: red, green, yellow, blue, pink, cyan, white, or off.")
            return
        
        # Convert text to SysEx message format
        # Ensure text is 7 characters or less
        if len(line_one_text) <= 7 :
            self.line_one_text = list(line_one_text.encode('ascii'))  # Convert to ASCII bytes
            if len(self.line_one_text) < 7:
                self.remaining_bytes = 7 - len(line_one_text)
                self.line_one_text.extend([0x00] * self.remaining_bytes)  # Pad with null bytes
                print(self.line_one_text)
        else:
            print("Text must be 7 characters or less.") 

        if len(line_two_text) <= 7:
            self.line_two_text = list(line_two_text.encode('ascii')) # Convert to ASCII bytes
            if len(self.line_two_text) < 7:
                self.remaining_bytes = 7 - len(line_two_text)
                self.line_two_text.extend([0x00] * self.remaining_bytes) # Pad with null bytes
        else:
            print("Text must be 7 characters or less.")


        # Convert text to SysEx message format
        message = [0xF0, 0x00, 0x00, 0x66, 0x58]  # Start byte, manufacturer ID, and scribble header
        message.append(self.channel)  # Channel byte
        message.append(self.color)  # Color byte
        message.extend(self.line_one_text)  # Line one text bytes
        message.extend(self.line_two_text)  # Line two text bytes
        message.append(0xF7)  # End byte
        print(message)  # Debug: Print the entire SysEx message for verification

        self.send_sysex_message(message)  # Send the SysEx message

        config = {
        "color": color,
        "second_line_inverted": second_line_inverted,
        "line_one_text": line_one_text,
        "line_two_text": line_two_text,
        }
        self.config_manager.set_scribble_strip_config(page_index, channel, config)