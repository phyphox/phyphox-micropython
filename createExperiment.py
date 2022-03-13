import phyphoxBLE
import phyphoxBleExperiment
import time
import random

p = phyphoxBLE.PhyphoxBLE()
editValue = 0.0
firstCall = True

def main():
    # Name max length is 26 characters
    p.start("My Device")
    p._write_callback = receivedData
    
    #Experiment
    plotRandomValues = phyphoxBleExperiment.PhyphoxBleExperiment()   #generate experiment on Arduino which plot random values
    plotRandomValues.setTitle("Random Number Plotter")
    plotRandomValues.setCategory("Arduino Experiments")
    plotRandomValues.setDescription("Random numbers are generated on Arduino and visualized with phyphox afterwards")
    plotRandomValues.setConfig("F0F0F0")

    #View
    firstView = phyphoxBleExperiment.PhyphoxBleExperiment.View()
    firstView.setLabel("FirstView") #Create a "view"
    secondView = phyphoxBleExperiment.PhyphoxBleExperiment.View()
    secondView.setLabel("SecondView") #Create a "view"

    #Graph
    firstGraph = phyphoxBleExperiment.PhyphoxBleExperiment.Graph()   #Create graph which will plot random numbers over time
    firstGraph.setLabel("Random number over time")
    firstGraph.setUnitX("s")
    firstGraph.setUnitY("")
    firstGraph.setLabelX("time")
    firstGraph.setLabelY("random number")
    firstGraph.setXPrecision(1)                 #The amount of digits shown after the decimal point
    firstGraph.setYPrecision(1)

    firstGraph.setChannel(0, 1)

    #Second Graph
    secondGraph = phyphoxBleExperiment.PhyphoxBleExperiment.Graph()   #Create graph which will plot random numbers over time
    secondGraph.setLabel("Random number squared over random number")
    secondGraph.setUnitX("")
    secondGraph.setUnitY("")
    secondGraph.setLabelX("random number")
    secondGraph.setLabelY("squared")
    secondGraph.setStyle("dots")
    secondGraph.setColor("2E728E")                #Sets Color of line

    secondGraph.setChannel(1, 2)

    #Info
    myInfo = phyphoxBleExperiment.PhyphoxBleExperiment.InfoField()     #Creates an info-box.
    myInfo.setInfo("In this view you can set a value between 1 and 10. The squared random value will be multiplied by this value and can be seen here.")
    #myInfo.setColor("404040")                   #Sets font color. Uses a 6 digit hexadecimal value in "quotation marks".
    myInfo.setXMLAttribute("size=\"1.2\"")

    #Separator
    mySeparator = phyphoxBleExperiment.PhyphoxBleExperiment.Separator()      #Creates a line to separate elements.
    mySeparator.setHeight(0.3)                       #Sets height of the separator.
    mySeparator.setColor("404040")                   #Sets color of the separator. Uses a 6 digit hexadecimal value in "quotation marks".

    #Value
    myValue = phyphoxBleExperiment.PhyphoxBleExperiment.Value()  #Creates a value-box.
    myValue.setLabel("Number")                  #Sets the label
    myValue.setPrecision(2)                     #The amount of digits shown after the decimal point.
    myValue.setUnit("u")                        #The physical unit associated with the displayed value.
    myValue.setColor("FFFFFF")                  #Sets font color. Uses a 6 digit hexadecimal value in "quotation marks".
    myValue.setChannel(3)
    myValue.setXMLAttribute("size=\"2\"")

    #Edit
    myEdit = phyphoxBleExperiment.PhyphoxBleExperiment.Edit() 
    myEdit.setLabel("Editfield")
    myEdit.setUnit("u")
    myEdit.setSigned(False)
    myEdit.setDecimal(False)
    myEdit.setChannel(1)
    myEdit.setXMLAttribute("max=\"10\"")

    #Export
    mySet = phyphoxBleExperiment.PhyphoxBleExperiment.ExportSet()        #Provides exporting the data to excel etc.
    mySet.setLabel("mySet")

    myData1 = phyphoxBleExperiment.PhyphoxBleExperiment.ExportData() 
    myData1.setLabel("myData1")
    myData1.setDatachannel(1)

    myData2 = phyphoxBleExperiment.PhyphoxBleExperiment.ExportData() 
    myData2.setLabel("myData2")
    myData2.setDatachannel(2)

    #attach to experiment

    firstView.addElement(firstGraph)            #attach graph to view
    firstView.addElement(secondGraph)            #attach second graph to view
    secondView.addElement(myInfo)                #attach info to view
    secondView.addElement(mySeparator)          #attach separator to view
    secondView.addElement(myValue)               #attach value to view
    secondView.addElement(myEdit)               #attach editfield to view (Linked to value)
    plotRandomValues.addView(firstView)         #attach view to experiment
    plotRandomValues.addView(secondView)
    mySet.addElement(myData1)                   #attach data to exportSet
    mySet.addElement(myData2)                   #attach data to exportSet
    plotRandomValues.addExportSet(mySet)        #attach exportSet to experiment
    p.addExperiment(plotRandomValues) #attach experiment to server
    
    i = 0
    while True:
        randomNumber = random.randint(0,100)                               #Generate random number in the range 0 to 100
        randomTimesEdit = randomNumber*editValue
        p.write(randomNumber, randomNumber*randomNumber, randomTimesEdit)  #Send value to phyphox
        time.sleep_ms(500)                                                 #Shortly pause before repeating


def receivedData():          # get data from PhyPhox app
    global editValue
    global firstCall
    if not firstCall:
        editValue = float(p.read())
    firstCall = False
    
if __name__ == "__main__":
    main()
