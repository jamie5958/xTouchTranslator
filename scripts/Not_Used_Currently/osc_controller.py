from pythonosc import udp_client

def create_osc_client(ip, port):
    return udp_client.SimpleUDPClient(ip, port)

def send_osc_message(client, address, value):
    client.send_message(address, value)

# Additional functions for handling OSC messages
