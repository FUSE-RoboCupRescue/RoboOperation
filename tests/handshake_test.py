import serial
import time

# Update '/dev/ttyACM0' to your Teensy port
# You can find it by running 'ls /dev/tty*' in terminal
PORT = '/dev/ttyACM0' 
BAUD = 115200

try:
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        print(f"Connecting to Teensy on {PORT}...")
        time.sleep(2)  # Give the connection a moment to stabilize

        # --- THE HANDSHAKE ---
        print("Waiting for 'Ready' signal from Teensy...")
        while True:
            if ser.in_waiting > 0:
                signal = ser.read(1).decode('utf-8')
                if signal == 'R':
                    print("Handshake received! Sending data...")
                    break
        
        # --- SENDING DATA ---
        message = "HELLO TEENSY\n"
        ser.write(message.encode('utf-8'))

        # --- RECEIVING ACK ---
        response = ser.readline().decode('utf-8').strip()
        print(f"Teensy says: {response}")

except serial.SerialException as e:
    print(f"Error: {e}")