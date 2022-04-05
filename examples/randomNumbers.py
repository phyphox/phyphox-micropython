from phyphoxBLE import PhyphoxBLE, Experiment
import time
import random

def main():
    p = PhyphoxBLE()
    p.start()                                #Start the BLE server
        
    while True:
        randomNumber = random.randint(0,100) #Generate random number in the range 0 to 100
        
        p.write(randomNumber)                #Send value to phyphox
        time.sleep_ms(500)                   #Shortly pause before repeating
            
if __name__ == "__main__":
    main()
