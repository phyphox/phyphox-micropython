import phyphoxBLE
import bluetooth
import time

def demo():
    ble = bluetooth.BLE()
    # Name max length is 26 characters, name is "phyphox" in app
    p = phyphoxBLE.PhyphoxBLE(ble, name="abcdefghijklmnopqrstuvwxyz")
    
    i = 0
    while True:
        p.read()
        if p.is_connected():
            # Short burst of queued notifications.
            for _ in range(3):
                p.write(i,i/7,"Hi")
                i += 1
        time.sleep_ms(2000)
            


if __name__ == "__main__":
    demo()
