import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    config = {}

                # Check if midi_in, midi_out, or midi_virtual exist in the loaded config, if not, set them to None
                if 'midi_in' not in config:
                    config['midi_in'] = None
                if 'midi_out' not in config:
                    config['midi_out'] = None
                if 'midi_virtual' not in config:
                    config['midi_virtual'] = None
                if 'scribble_strips' not in config:
                    config['scribble_strips'] = {}  # Add a default empty dictionary for scribble strips
                return config
        else:
            # Return a default config with None values if the file doesn't exist
            return {'midi_in': None, 'midi_out': None, 'midi_virtual': None, 'scribble_strips': {}}

    def save_config(self, midi_in=None, midi_out=None, midi_virtual=None):
        # Update the config with new values if provided
        if midi_in is not None:
            self.config['midi_in'] = midi_in
        if midi_out is not None:
            self.config['midi_out'] = midi_out
        if midi_virtual is not None:
            self.config['midi_virtual'] = midi_virtual
        try:
            with open(CONFIG_PATH, 'w') as f:
                json.dump(self.config, f, indent=4)
            print("Configuration saved successfully.")
        except IOError as e:
            print(f"Error saving config: {e}")

    def get_midi_in(self):
        return self.config.get('midi_in')

    def get_midi_out(self):
        return self.config.get('midi_out')
    
    def get_midi_virtual(self):
        return self.config.get('midi_virtual')
    
    def set_midi_in(self, midi_in_device):
        self.config['midi_in'] = midi_in_device
        self.save_config()

    def set_midi_out(self, midi_out_device):
        self.config['midi_out'] = midi_out_device
        self.save_config()

    def set_midi_virtual(self, midi_virtual_device):
        self.config['midi_virtual'] = midi_virtual_device
        self.save_config()

    def set_scribble_strip_config(self, page_index, fader_index, config):
        """
        Save the configuration for a specific fader's scribble strip.
        :param page_index: The index of the page (0-13).
        :param fader_index: The index of the fader (0-7).
        :param config: A dictionary containing the scribble strip configuration.
        """
        if 'scribble_strips' not in self.config:
            self.config['scribble_strips'] = {}
        # Ensure the page exists in the config
        if f"page_{page_index}" not in self.config['scribble_strips']:
            self.config['scribble_strips'][f"page_{page_index}"] = {}

        # Save the fader configuration for the page
        self.config['scribble_strips'][f"page_{page_index}"][f"fader_{fader_index}"] = config
        self.save_config()

    def get_scribble_strip_config(self, page_index, fader_index):
        """
        Retrieve the configuration for a specific fader's scribble strip on a specific page.
        :param page_index: The index of the page (0-13).
        :param fader_index: The index of the fader (0-7).
        :return: A dictionary containing the scribble strip configuration.
        """
        return self.config.get('scribble_strips', {}).get(f"page_{page_index}", {}).get(
            f"fader_{fader_index}",
            {"color": "off", "second_line_inverted": False, "line_one_text": "", "line_two_text": ""}
        )