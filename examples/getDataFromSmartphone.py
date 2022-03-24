import phyphox
import machine
import time

p = phyphox.PhyphoxBLE()
lastTimestamp = 0
blinkInterval = 1000
led = True
ledPin = 22
p.debug = True

def main():
    global lastTimestamp
    global led
    p.start("My Device")
    p._write_callback = receivedData
    buildInLed = machine.Pin(ledPin, machine.Pin.OUT)    
    
    #Experiment
    getDataFromSmartphone = phyphox.PhyphoxBLEExperiment()   #generate experiment on Arduino which plot random values
    getDataFromSmartphone.setTitle("Set Blink Interval")
    getDataFromSmartphone.setCategory("Micropython Experiments")
    getDataFromSmartphone.setDescription("User can set Blink Interval of Mikrocontroller LED")    

    #View
    firstView = phyphox.PhyphoxBLEExperiment.View()
    firstView.setLabel("FirstView") #Create a "view"

    #Edit
    Interval = phyphox.PhyphoxBLEExperiment.Edit() 
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
            lastTimestamp = time.ticks_ms();
            led = not led;
            buildInLed.value(led)

def receivedData():          # get data from PhyPhox app
    global blinkInterval
    receivedInterval = p.read()
    if receivedInterval > 0 and receivedInterval != blinkInterval:
        print("New Interval: ", receivedInterval)
        blinkInterval = receivedInterval


if __name__ == "__main__":
    main()

