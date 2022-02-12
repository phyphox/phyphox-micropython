import phyphoxBLE
import phyphoxBleExperiment
import time

def demo():
    # Name max length is 26 characters
    p = phyphoxBLE.PhyphoxBLE()
    p.start("Write Test")
    
    i = 0
    while True:
        #a=p.read_array(3)
        #print(a)
        if p.is_connected():
            p.when_subscription_received()
            # Short burst of queued notifications.
            for _ in range(3):
                p.write(i,i/7,3.14*i)
                i += 1
        time.sleep_ms(2000)
            


if __name__ == "__main__":
    demo()


