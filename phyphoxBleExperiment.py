from io import StringIO

phyphoxBleNViews      = 5
phyphoxBleNElements   = 5
phyphoxBleNExportSets = 5

class PhyphoxBleExperiment:
    def __init__(self):
      self._TITLE          = "MPY-Experiment"
      self._CATEGORY       = "MPY Experiments"
      self._DESCRIPTION    = "An experiment created with the phyphox BLE library for mpy-compatible micro controllers"
      self._CONFIG         = "000000"
      self._VIEWS          = [0]*phyphoxBleNViews
    
    @property
    def TITLE(self):
      return self._TITLE
    
    def CATEGORY(self):
      return self._CATEGORY
    
    def DESCRIPTION(self):
      return self._DESCRIPTION
    
    def CONFIG(self):
      return self._CONFIG
    
    def VIEWS(self):
      return self._VIEWS
    
    def setTitle(self, strInput):
        self._TITLE = strInput
    
    def getFirstBytes(self, buffer, device_name):
      #header
      buffer.write('<phyphox version=\"1.10\">\n')
      #title
      buffer.write('<title>')
      buffer.write(self._TITLE)
      buffer.write('<\title>\n')
      #category
      buffer.write('<category>')
      buffer.write(self._CATEGORY)
      buffer.write('<\category>\n')
      #description
      buffer.write('<description>')
      buffer.write(self._DESCRIPTION)
      buffer.write('<\description>\n')
      #container
      buffer.write('data-containers>\n')
      buffer.write('\t<container size=\"0\" static=\"false\">CH1</container>\n \
                    \t<container size=\"0\" static=\"false\">CH2</container>\n \
                    \t<container size=\"0\" static=\"false\">CH3</container>\n \
                    \t<container size=\"0\" static=\"false\">CH4</container>\n \
                    \t<container size=\"0\" static=\"false\">CH0</container>\n \
                    \t<container size=\"0\" static=\"false\">CH1</container>\n')
      buffer.write('<\data-container>\n')
      #input
      buffer.write('<input>\n')
      buffer.write('\t<bluetooth name=\"')
      buffer.write(device_name)
      buffer.write('\" mode=\"notification\" rate=\"1\" subscribeOnStart=\"false\">\n')
      #config
      buffer.write('\t\t<config char=\"cddf1003-30f7-4671-8b43-5e40ba53514a\" conversion=\"hexadecimal\">')
      buffer.write(self._CONFIG)
      buffer.write('</config>\n\t\t')
      for i in range(5):
        buffer.write('<output char=\"cddf1002-30f7-4671-8b43-5e40ba53514a\" conversion=\"float32LittleEndian\" ')
        k = i*4
        tmp = "offset=\"%i\" >CH%i" % (k,i+1)
        buffer.write(tmp)
        buffer.write('</output>\n\t\t')
      buffer.write('<output char=\"cddf1002-30f7-4671-8b43-5e40ba53514a\" extra=\"time\">CH0</output>\n')
      buffer.write('\t</bluetooth>\n')
      buffer.write('</input>\n')
      #output
      buffer.write('<output>\n')
      buffer.write('\t<bluetooth name=\"')
      buffer.write(device_name)
      buffer.write('\">\n')
      buffer.write('\t\t<input char=\"cddf1003-30f7-4671-8b43-5e40ba53514a\" conversion=\"float32LittleEndian\">CB1</input>\n')
      buffer.write('\t</bluetooth>\n')
      buffer.write('</output>\n')
      #analysis
      buffer.write('<analysis sleep=\"0\"  onUserInput=\"false\"></analysis>\n')
      #views
      buffer.write('<views>\n')

# 	//build views
# 	strcat(buffArray, "<views>\n");
# 
# 	//errorhandling
# 	for(int i=0;i<phyphoxBleNViews;i++) {
# 		for(int j=0;j<phyphoxBleNElements;j++) {
# 			if(VIEWS[i]!= nullptr && errors<=2){
# 				if(VIEWS[i]->ELEMENTS[j]!=nullptr){
# 					if(strcmp(VIEWS[i]->ELEMENTS[j]->ERROR.MESSAGE, "") != 0) {
# 						if(errors == 0) {
# 							strcat(buffArray, "\t<view label=\"ERRORS\"> \n");
# 						}
# 						VIEWS[i]->ELEMENTS[j]->ERROR.getBytes(buffArray);
# 						errors++;
# 					}
# 				}
# 			}
# 		}
# 	}
# 	if(errors>0) {
# 		strcat(buffArray,"\t\t<info  label=\"DE: Siehe Dokumentation für mehr Informationen zu Fehlern.\">\n");
# 		//strcat(buffArray,"\" color=\"ff0000\">\n");
# 		strcat(buffArray,"\t\t</info>\n");
# 		strcat(buffArray,"\t\t<info  label=\"EN: Please check the documentation for more information about errors.\">\n");
# 		//strcat(buffArray,"\" color=\"ff0000\">\n");
# 		strcat(buffArray,"\t\t</info>\n");
# 		strcat(buffArray,"\t</view>\n");
# 	}
      
      
    def getViewBytes(self, buffer, v, e):
      print("Not implemented yet")
        
    def getLastBytes(self, buffer):
      print("Not implemented yet")
        
    def addView(self, v):
      print("Not implemented yet")
    
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
A.getFirstBytes(buffer,"name")
for i in range(phyphoxBleNElements):
  V.getBytes(buffer,i)
print(buffer.getvalue())




