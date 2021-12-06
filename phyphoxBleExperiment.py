from io import StringIO

phyphoxBleNViews      = 5
phyphoxBleNElements   = 5
phyphoxBleNExportSets = 5

class PhyphoxBleExperiment:
    MESSAGE = ""

    def getBytes(self,byteString):
        return byteString
    
    class View:
      def __init__(self):
        self._LABEL         = ""
        self._XMLATTRIBUTE  = ""
        self._ELEMENTS = [0]*phyphoxBleNElements
        
      @property
      def LABEL(self):
        return self._LABEL
    
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
    
      def ELEMENTS(self):
        return self._ELEMENTS
    
      def addElement(self, e):
        for i in range(phyphoxBleNElements):
          if not self._ELEMENTS[i]:
            self._ELEMENTS[i] = e
            break
    
    
      def setLabel(self, strInput):
        self._LABEL = " label=\"" + strInput + "\""
    
      def setXMLAttribute(self, strInput):
        self._XMLATTRIBUTE = " " + strInput
      
      def getBytes(self, buffer, elem):
        if elem == 0:
          buffer.write('\t<view')
          buffer.write(self._LABEL)
          buffer.write(self._XMLATTRIBUTE)
          buffer.write('>\n')
        if self._ELEMENTS[elem]:
            print("")
            self._ELEMENTS[elem].getBytes(buffer)
        if elem == phyphoxBleNElements-1:
          buffer.write('\t</view>\n')
    
    
    class Element:
      def __init__(self):
        self._TYPEID        = 0
        self._LABEL         = ""
      
      @property
      def TYPEID(self):
        return self._TYPEID
        
      def LABEL(self):
        return self._LABEL
    
      def setLabel(self, strInput):
        self._LABEL = " label=\"" + strInput + "\""      
      
    class Graph(Element):
      def __init__(self):
        super().__init__()
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
        return self._LABELX
        
      def LABELY(self):
        return self._LABELY
        
      def COLOR(self):
        return self._COLOR
        
      def XPRECISION(self):
        return self._XPRECISION
        
      def YPRECISION(self):
        return self._YPRECISION
        
      def INPUTX(self):
        return self._INPUTX
        
      def INPUTY(self):
        return self._INPUTY
        
      def STYLE(self):
        return self._STYLE
        
      def XMLATTRIBUTE(self):
        return self._XMLATTRIBUTE
        
        
        
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
        self._XMLATTRIBUTE = " " + strInput
      
      def getBytes(self, buffer):
        buffer.write('\t\t<graph')
        buffer.write(self._LABEL)
        buffer.write(self._LABELX)
        buffer.write(self._LABELY)
        buffer.write(' labelZ=\"\"')
        buffer.write(self._UNITX)
        buffer.write(self._UNITY)
        buffer.write(self._XPRECISION)
        buffer.write(self._YPRECISION)
        buffer.write(self._STYLE)
        buffer.write(self._COLOR)
        buffer.write(self._XMLATTRIBUTE)
        buffer.write('>\n')
        buffer.write('\t\t\t<input axis=\"x\">')
        buffer.write(self._INPUTX)
        buffer.write('"</input>\n\t\t\t<input axis=\"y\">')
        buffer.write(self._INPUTY)
        buffer.write('</input>\n\t\t</graph>\n')






#Just for debugging
buffer = StringIO()
A = PhyphoxBleExperiment();
V = PhyphoxBleExperiment.View()
G = PhyphoxBleExperiment.Graph()
G.setLabelX("tmpLabel")
G.setXMLAttribute("unitY=\"m\"")
G.setChannel(1,2)
G.setLabel("test")
V.addElement(G)
for i in range(phyphoxBleNElements):
  V.getBytes(buffer,i)
print(buffer.getvalue())




