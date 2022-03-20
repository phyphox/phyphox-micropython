import phyphox
import machine
import time

p = phyphox.PhyphoxBLE()
lastTimestamp = 0;
blinkInterval = 1000;
led = True;

def main():
    global lastTimestamp
    global led
    p.start("My Device")
    p._write_callback = receivedData
    buildInLed = machine.Pin(2, machine.Pin.OUT)
    
    #Experiment
    getDataFromSmartphone = phyphox.PhyphoxBleExperiment()   #generate experiment on Arduino which plot random values
    getDataFromSmartphone.setTitle("Set Blink Interval")
    getDataFromSmartphone.setCategory("Micropython Experiments")
    getDataFromSmartphone.setDescription("User can set Blink Interval of Mikrocontroller LED")    

    #View
    firstView = phyphox.PhyphoxBleExperiment.View()
    firstView.setLabel("FirstView") #Create a "view"

    #Edit
    Interval = phyphox.PhyphoxBleExperiment.Edit() 
    Interval.setLabel("Interval")
    Interval.setUnit("ms")
    Interval.setSigned(False)
    Interval.setDecimal(False)
    Interval.setChannel(1)

    firstView.addElement(Interval)
    getDataFromSmartphone.addView(firstView)
    p.addExperiment(getDataFromSmartphone)

    while True:
        if time.ticks_ms()-lastTimestamp > blinkInterval:
            print(blinkInterval)
            lastTimestamp = time.ticks_ms();
            led = not led;
            if led:
                buildInLed.value(1)
                print("led on")
            else:
                buildInLed.value(0)          
                print("led off")

def receivedData():          # get data from PhyPhox app
    global blinkInterval
    receivedInterval = float(p.read())
    if receivedInterval > 0:
        blinkInterval = receivedInterval
    print(blinkInterval)



if __name__ == "__main__":
    main()
