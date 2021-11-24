class PhyphoxBleExperiment:
    MESSAGE = ""

    def getBytes(self,byteString):
      return byteString
      
    class Graph:
      def __init__(self):
        self._UNITX         = ""
        self._UNITY         = ""
        self._LABELX        = ""
        self._LABELY        = ""
        self._COLOR         = ""
        self._XPRECISION    = ""
        self._YPRECISION    = ""
        self._INPUTX        = "CH0"
        self._INPUTY        = "CH1"
        self._STYLE         = ""
        self._XMLATTRIBUTE  = ""
       
      @property
      def UNITX(self):
        return self._UNITX
        
      def UNITY(self):
        return self._UNITY
        
      def LABELX(self):
        return self._UNITX
        
      def LABELY(self):
        return self._UNITY
        
      def COLOR(self):
        return self._UNITY
        
      def XPRECISION(self):
        return self._UNITY
        
      def YPRECISION(self):
        return self._UNITY
        
      def INPUTX(self):
        return self._UNITY
        
      def INPUTY(self):
        return self._UNITY
        
      def STYLE(self):
        return self._UNITY
        
      def XMLATTRIBUTE(self):
        return self._UNITY
        
        
        
      def setUnitX(self, strInput):
        self._UNITX = " unitX=\"" + strInput + "\""
       
      def setUnitY(self, strInput):
        self._UNITY = " unitY=\"" + strInput + "\""
        
      def setLabelX(self, strInput):
        self._LABELX = " labelX=\"" + strInput + "\""
        
      def setLabelY(self, strInput):
        self._LABELY = " labelY=\"" + strInput + "\""
        
      def setColor(self, strInput):
        self._COLOR = " color=\"" + strInput + "\""
        
      def setXPrecision(self, intInput):
        self._XPRECISION = " xPrecision=\"" + intInput + "\""
        
      def setYPrecision(self, intInput):
        self._YPRECISION = " yPrecision=\"" + intInput + "\""
        
      def setChannel(self, intInputX, intInputY):
        self._INPUTX = "CH" + str(intInputX)
        self._INPUTY = "CH" + str(intInputY)
        
      def setStyle(self, strInput):
        self._STYLE = " style=\"" + strInput + "\""
        
      def setXMLAttribute(self, strInput):
        self._STYLE = " " + strInput
      
      #TODO: add Label from parentclass Element
      def getBytes(self, buffer):
        buffer = "" + buffer + "\t\t<graph" + self._LABELX + self._LABELY + " labelZ=\"\"" + \
          self._UNITX + self._UNITY + self._XPRECISION + self._YPRECISION + self._STYLE + \
          self._COLOR + self._XMLATTRIBUTE + ">\n" + "\t\t\t<input axis=\"x\">" + self._INPUTX + \
          "</input>\n\t\t\t<input axis=\"y\">" + self._INPUTY + "</input>\n\t\t</graph>\n"
        return buffer                                                                          #FRAGE: Kein Pointer. Return als L枚sung? -> stringIO?

#Just for debugging
A = PhyphoxBleExperiment();
G = PhyphoxBleExperiment.Graph()
G.setLabelX("tmpLabel")
G.setXMLAttribute("unitY=\"m\"")
G.setChannel(1,2)
buff = G.getBytes("")

print(buff)


