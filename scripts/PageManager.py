import rtmidi

class PageManager:
    def __init__(self, config_manager, sysex_controller):
        """
        Initialize the PageManager with a ConfigManager instance.
        :param config_manager: An instance of ConfigManager to handle persistent storage.
        """
        self.config_manager = config_manager
        self.sysex_controller = sysex_controller
        print(f"SysexController assigned: {self.sysex_controller is not None}")
        self.current_page = 0
        self.max_pages = 13  # Assuming 14 pages (0-13)
        self.page_change_callback = None  # Callback to notify when the page changes
        print(f"Initialized on Page {self.current_page}")

    def set_scribble_strip(self, fader_index, config):
        """
        Save the configuration for a specific fader on the current page.
        :param fader_index: The index of the fader (0-7).
        :param config: A dictionary containing the scribble strip configuration.
        """
        self.config_manager.set_scribble_strip_config(self.current_page, fader_index, config)

    def get_scribble_strip(self, fader_index):
        """
        Retrieve the configuration for a specific fader on the current page.
        :param fader_index: The index of the fader (0-7).
        :return: A dictionary containing the scribble strip configuration.
        """
        return self.config_manager.get_scribble_strip_config(self.current_page, fader_index)
    
    def update_scribble_strips(self):
        """
        Update the scribble strips for the current page using the saved configuration.
        """
        print(f"Updating scribble strips for Page {self.current_page}...")
        for fader_index in range(8):  # Assuming 8 faders per page
            config = self.get_scribble_strip(fader_index)
            self.sysex_controller.write_to_scribble_strip(
                self.current_page,
                fader_index,
                config["color"],
                config.get("second_line_inverted", False),
                config["line_one_text"],
                config["line_two_text"],
            )

    def change_page(self, direction):
        """
        Change the current page and ensure it stays within valid bounds.
        :param direction: 'next' to go to the next page, 'prev' to go to the previous page.
        """
        try:
            if direction == 'next':
                if self.current_page < self.max_pages - 1:
                    self.current_page += 1
                else:
                    print("Already on the last page")
            elif direction == 'prev':
                if self.current_page > 0:
                    self.current_page -= 1
                else:
                    print("Already on the first page")
            print(f"Switched to Page {self.current_page}")

            # Update the scribble strips for the new page
            self.update_scribble_strips()

            # Call the page change callback if it is set
            if self.page_change_callback:
                self.page_change_callback(self.current_page)

        except Exception as e:
            print(f"An error occurred while changing the page: {e}")