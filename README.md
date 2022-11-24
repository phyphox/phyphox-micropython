# phyphox Micropython BLE

Use phyphox to plot sensor data from your Microcontroller. 

The purpose of this library is to use the phyphox app (see www.phyphox.org) to plot sensor data on your phone with the open source app phyphox. In the other direction you can also use this library to access sensor data from your phone to use in your ESP32 project with [Micropython](https://micropython.org/).

## Supported boards
- ESP 32

## Concept of phyphox

Phyphox is an open source app that has been developed at the RWTH Aachen University. It is available on Android and iOS and primarily aims at making the phone's sensors available for physics experiments. However, the app is based on a very flexible file format that defines data sources, visualizations (i.e. values and graphs) and data analysis (from simple formulas to Fourier transforms). This file format also allows to define Bluetooth Low Energy devices to exchange data from and to.

This library generates an experiment configuration in this file format and allows phyphox to conenct to your microcontroller. It directly transfers the configuration (including graph configurations, axis labels, etc.) to phyphox and provides function to submit data to be plotted in phyphox or receive sensor data.

## Installation

* Installiere Thonny IDE.

## Usage

The easiest way to learn how to use this library is by looking at the examples in the `examples` folder. In most cases, you can simply connect to your Microcontroller running this library by scanning for Bluetooth devices via the "+"-button on the main screen of phyphox.

### randomNumbers.ino

This is our minimal example. It submits random numbers to phyphox. All you need to do to submit a value to phyphox is including this library, starting the server (i.e. in `setup()`) and writing your data to the server.

```python
import phyphoxBLE
import time
import random

def main():
    p = phyphoxBLE.PhyphoxBLE()
    p.start()                                #Start the BLE server
        
    while True:
        randomNumber = random.randint(0,100) #Generate random number in the range 0 to 100
        
        p.write(randomNumber)                #Send value to phyphox
        time.sleep_ms(500)                   #Shortly pause before repeating
            
if __name__ == "__main__":
    main()
```

### CreateExperiment.ino

This example shows how you can set a title, category and description as well as how to define graphs and setting axis labels and units. You can define one or multiple views (shown as tabs in phyphox), each of which can hold one or more graphs.

For each graph you need to call `setChannel(x, y)` with x and y being an index of your data set. This index corresponds to the order of the values that you transfer in a call to `server.write` while the index `0` is special and corresponds to the timestamp at which phyphox receives the value. At the moment `server.write` supports up to five values.

For example, let's assume you have the float values `foo` and `bar`. You can then call server.write(foo, bar) to send a set with both values. If you call `setChannel(0,1)`, your graph would plot `foo` on the y axis over time on the x axis. If you call `setChannel(2,1)`, your graph would plot `foo` on the y axis and `bar` on the x axis.

Here are some useful methods to create your own experiment:

| Target     | Method                   | Explanation                                                       |
| ---------- | ------------------------ | ----------------------------------------------------------------- |
| Experiment | setTitle(String)         | Sets a title for the experiment                                   |
| Experiment | setCategory(String)      | Sets a category for the experiment                                |
| Experiment | setDescription(String)   | Sets a description for the experiment                             |
| Experiment | addView(View)            | Adds a view to the corresponding experiment                       |
| Experiment | addExportSet(ExportSet)  | Adds an exportSet to the corresponding experiment                 |
| View       | addElement(Element)      | Adds an element to the corresponding view                         |
| View       | setLabel(String)         | Sets a label for the view                                         |
| Graph      | setLabel(String)         | Sets a label for the graph                                        |
| Graph      | setUnitX(String)         | Sets the unit for x (similar with y)                              |
| Graph      | setLabelX(String)        | Sets a label for x (similar with y)                               |
| Graph      | setXPrecision(int)       | Sets the amount of digits after the decimal point (similar with y)|
| Graph      | setChannel(int, int)     | As explained above (1-5)                                          |
| Graph      | setStyle(String)         | Sets the style. For more possibilities check the wiki             |
| Graph      | setColor(String)         | Sets the line color of the graph (use a 6 digit hexadecimal code) |
| Separator  | setHeight(float)         | Creates a line to separate parts of the experiment                |
| Separator  | setColor(String)         | Sets the color of the line (use a 6 digit hexadecimal code)       |
| Info       | setInfo(String)          | Sets the infotext                                                 |
| Info       | setColor(String)         | Sets the font color (use a 6 digit hexadecimal code)              |
| Value      | setLabel(String)         | Sets a label for the displayed value                              |
| Value      | setPrecision(int)        | Sets the amount of digits after the decimal point                 |
| Value      | setUnit(String)          | Sets a unit for the displayed value                               |
| Value      | setColor(String)         | Sets the font color (use a 6 digit hexadecimal code)              |
| Value      | setChannel(int)          | As explained above, just with one parameter (1-5)                 |
| Edit       | setLabel(String)         | Sets label for the editfield                                      |
| Edit       | setUnit(String)          | Sets unit                                                         |
| Edit       | setSigned(bool)          | true = signed values allowed                                      |
| Edit       | setDecimal(bool)         | true = decimal values allowed                                     |
| Edit       | setChannel(int)          | As explained above, just with one parameter (1-5)                 |
| ExportSet  | setLabel(String)         | Sets a label for the exportSet (Used to export to Excel, etc.)    |
| ExportData | setLabel(String)         | Sets a label for the exportData                                   |
| ExportData | setDatachannel(int)      | Defines which channel should be exported for this dataset (1-5)   |
| Everything | setXMLAttribute(String)  | Custom property e.g. setXMLAttribute("lineWidth=\"3\"")           |

If for some reason the app shows you an error in form of "ERROR FOUND: ERR_X", with different values for X, this could be the reason:
* ERR_01: The input was too long
* ERR_02: The value exceeds the upper limit
* ERR_03: The input was not a 6-digit hexadecimal code
* ERR_04: The input does not match with a valid value

If the microcontroller is continiously rebooting, you maybe added too many elements.

### getDataFromSmartphone.ino

The phyphox file format is much more powerful than what is offered by this library's interface. In the example `getDataFromSmartphone.ino` you can see how a phyphox-file can be used to set up a sensor on the phone and retrieve its data on the microcontroller.

As the phyphox file format is extremely complex and powerful, please refer to the [phyphox wiki](https://phyphox.org/wiki/index.php/Phyphox_file_format) to learn about it and feel free to contact us if you are stuck or think that a specific aspect of the file format should be easily accessible through our Micropython library.

### Further documentation

For now, this library is rather lightweight. Feel free to browse the files to learn about the functions that are already available.

## Missing features

In the future we would like to see...
- Some memory optimization
- Compression for the transfer of the phyphox experiment generated on the microcontroller
- Option to request a larger mtu size
- Addition graph settings
- Proper documentation

If you can help with this, we are happy to receive a pull request. You can contact us via contact@phyphox.org if you plan on a large addition to this library and want to make sure that it does not collide with anything we are already working on.

## Credits

This library has been developed by the phyphox team at the RWTH Aachen University. It is a port of our [Arduino BLE library](https://github.com/phyphox/phyphox-arduino) and has been developed by Edward Leier and Marcel Hagedorn.

## Contact

Contact us any time at contact@phyphox.org and learn more about phyphox on https://phyphox.org.

## Licence

This library is released under the GNU Lesser General Public Licence v3.0 (or newer).

Note that it uses MicroPython and uses code from its Bluetooth examples (specifically [ble_advertising.py](https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_advertising.py), which are licenced under the MIT licence as listed at the end of this readme

## Third-party licences

MicroPython is licenced under the MIT licence.

The MIT License (MIT)

Copyright (c) 2013-2022 Damien P. George

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
