import time
import threading
import rtmidi

class Handshake:
    def __init__(self, midi_out):
        self.midi_out = midi_out

        # SysEx Handshake Message
        self.handshake_message = [0xF0, 0x00, 0x00, 0x66, 0x14, 0x00, 0xF7]
        
        self.running = False
        self.thread = None

    def send_handshake(self):
            # print("Sending SysEx Handshake...")
            self.midi_out.send_message(self.handshake_message)

    def start_handshake(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target = self.handshake_loop)
        self.thread.start()

    def handshake_loop(self):
        print("Started SysEx Handshake. Press Ctrl+C to stop.")
        while self.running:
            self.send_handshake()
            for _ in range(60):  # Break 6 seconds into 60 smaller intervals (0.1 seconds each)
                if not self.running:
                    break
                time.sleep(0.1)

    def stop_handshake(self):
        self.running = False
        print("Stopped SysEx Handshake.")